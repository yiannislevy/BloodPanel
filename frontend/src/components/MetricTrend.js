import React, { useEffect, useState } from 'react';
import { fetchSessions } from '../api';
import { areTestNamesSimilar } from '../utils/stringUtils';

const MetricTrend = ({ testName, onClose }) => {
  const [trendData, setTrendData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTrendData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Fetch all sessions
        const sessions = await fetchSessions();
        
        // For each session, fetch details and find matching test
        const detailsPromises = sessions.map(async session => {
          try {
            const response = await fetch(`http://localhost:8000/sessions/${session.session_id}`);
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
          } catch (e) {
            console.error(`Failed to fetch session ${session.session_id}:`, e);
            return null;
          }
        });
        
        const allSessionDetails = await Promise.all(detailsPromises);
        
        // Extract matching tests using fuzzy matching
        const matchingTests = allSessionDetails
          .filter(Boolean) // Remove failed requests
          .map((session, index) => {
            if (!session || !session.blood_tests) return null;
            
            const matchingTest = session.blood_tests.find(test => 
              areTestNamesSimilar(test.test_name, testName)
            );
            
            if (matchingTest) {
              return {
                date: new Date(sessions[index].test_date),
                value: parseFloat(matchingTest.value),
                unit: matchingTest.unit
              };
            }
            return null;
          })
          .filter(Boolean);

        // Sort by date
        matchingTests.sort((a, b) => a.date - b.date);
        setTrendData(matchingTests);
      } catch (error) {
        console.error('Error fetching trend data:', error);
        setError('Failed to load trend data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchTrendData();
  }, [testName]);

  if (loading) return <div>Loading trend data...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div style={{
      position: 'fixed',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      backgroundColor: 'white',
      padding: '20px',
      borderRadius: '10px',
      boxShadow: '0 0 10px rgba(0,0,0,0.2)',
      maxWidth: '600px',
      width: '90%'
    }}>
      <button 
        onClick={onClose}
        style={{
          position: 'absolute',
          right: '10px',
          top: '10px',
          cursor: 'pointer'
        }}
      >
        ✕
      </button>
      <h3>Trend for {testName}</h3>
      {trendData.length === 0 ? (
        <p>No historical data found for this test.</p>
      ) : (
        <div style={{ marginTop: '20px' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th>Date</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              {trendData.map((data, index) => (
                <tr key={index}>
                  <td>{data.date.toLocaleDateString()}</td>
                  <td>{data.value} {data.unit}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default MetricTrend; 