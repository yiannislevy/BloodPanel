// SessionDetails.js
import React, { useEffect, useState } from 'react';
import { fetchSessionDetails } from '../api';
import MetricTrend from './MetricTrend';

const SessionDetails = ({ sessionId }) => {
  const [details, setDetails] = useState(null);
  const [selectedTest, setSelectedTest] = useState(null);

  useEffect(() => {
    fetchSessionDetails(sessionId).then(data => setDetails(data));
  }, [sessionId]);

  if (!details) return <p>Loading...</p>;

  const testItemStyle = {
    cursor: 'pointer', 
    padding: '5px',
    margin: '5px 0',
    borderRadius: '5px',
    transition: 'background-color 0.2s'
  };

  return (
    <div style={{ width: '60%', border: '1px solid #ddd', padding: '15px', borderRadius: '10px' }}>
      <h3>Test Results on {new Date(details.test_date).toLocaleDateString()}</h3>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {details.blood_tests.map(test => (
          <li 
            key={test.test_id}
            onClick={() => setSelectedTest(test.test_name)}
            style={testItemStyle}
            onMouseEnter={e => e.target.style.backgroundColor = '#f0f0f0'}
            onMouseLeave={e => e.target.style.backgroundColor = 'transparent'}
          >
            🔬 <strong>{test.test_name}</strong>: {test.value} {test.unit} 
            {test.normal_range && ` (Normal: ${test.normal_range})`}
          </li>
        ))}
      </ul>

      {selectedTest && (
        <MetricTrend 
          testName={selectedTest} 
          onClose={() => setSelectedTest(null)}
        />
      )}
    </div>
  );
};

export default SessionDetails;
