// SessionDetails.js
import React, { useEffect, useState } from 'react';
import { fetchSessionDetails, updateBloodTest } from '../api';
import MetricTrend from './MetricTrend';

const SessionDetails = ({ sessionId }) => {
  const [details, setDetails] = useState(null);
  const [selectedTest, setSelectedTest] = useState(null);
  const [editingTest, setEditingTest] = useState(null);
  const [editValue, setEditValue] = useState('');
  const [isUpdating, setIsUpdating] = useState(false);

  useEffect(() => {
    fetchSessionDetails(sessionId).then(data => setDetails(data));
  }, [sessionId]);

  const handleEdit = (test) => {
    setEditingTest(test);
    setEditValue(test.value);
  };

  const handleSave = async (test) => {
    setIsUpdating(true);
    try {
      const updatedData = {
        value: editValue,
        unit: test.unit,
        test_name: test.test_name
      };

      await updateBloodTest(sessionId, test.test_id, updatedData);
      
      // Refresh the details
      const newDetails = await fetchSessionDetails(sessionId);
      setDetails(newDetails);
      setEditingTest(null);
    } catch (error) {
      console.error('Error updating test:', error);
      alert('Failed to update test value');
    } finally {
      setIsUpdating(false);
    }
  };

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
            style={{
              padding: '10px',
              margin: '5px 0',
              borderRadius: '5px',
              backgroundColor: '#f8f9fa',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}
          >
            <div onClick={() => setSelectedTest(test.test_name)} style={{ cursor: 'pointer', flex: 1 }}>
              🔬 <strong>{test.test_name}</strong>: {' '}
              {editingTest?.test_id === test.test_id ? (
                <input
                  type="text"
                  value={editValue}
                  onChange={(e) => setEditValue(e.target.value)}
                  style={{ width: '80px' }}
                />
              ) : (
                <span>{test.value}</span>
              )}{' '}
              {test.unit} 
              {test.normal_range && ` (Normal: ${test.normal_range})`}
            </div>
            <div>
              {editingTest?.test_id === test.test_id ? (
                <button
                  onClick={() => handleSave(test)}
                  disabled={isUpdating}
                  style={{
                    marginLeft: '10px',
                    padding: '4px 8px',
                    backgroundColor: '#28a745',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer'
                  }}
                >
                  Save
                </button>
              ) : (
                <button
                  onClick={() => handleEdit(test)}
                  style={{
                    marginLeft: '10px',
                    padding: '4px 8px',
                    backgroundColor: '#007bff',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer'
                  }}
                >
                  Edit
                </button>
              )}
            </div>
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
