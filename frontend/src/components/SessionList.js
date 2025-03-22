// SessionList.js
import React, { useEffect, useState } from 'react';
import { fetchSessions } from '../api';

const SessionList = ({ onSelectSession }) => {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    fetchSessions().then(data => setSessions(data));
  }, []);

  return (
    <div style={{ width: '40%', border: '1px solid #ddd', padding: '15px', borderRadius: '10px' }}>
      <h3>Previous Sessions</h3>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {sessions.map(session => (
          <li key={session.session_id} style={{ cursor: 'pointer', marginBottom: '10px' }}
              onClick={() => onSelectSession(session.session_id)}>
            📅 {new Date(session.test_date).toLocaleDateString()} ({session.location || 'No location'})
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SessionList;
