// SessionDetails.js
import React, { useEffect, useState } from 'react';
import { fetchSessionDetails } from '../api';

const SessionDetails = ({ sessionId }) => {
  const [details, setDetails] = useState(null);

  useEffect(() => {
    fetchSessionDetails(sessionId).then(data => setDetails(data));
  }, [sessionId]);

  if (!details) return <p>Loading...</p>;

  return (
    <div style={{ width: '60%', border: '1px solid #ddd', padding: '15px', borderRadius: '10px' }}>
      <h3>Test Results on {new Date(details.test_date).toLocaleDateString()}</h3>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {details.blood_tests.map(test => (
          <li key={test.test_id}>
            🔬 <strong>{test.test_name}</strong>: {test.value} {test.unit} 
            {test.normal_range && `(Normal: ${test.normal_range})`}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SessionDetails;
