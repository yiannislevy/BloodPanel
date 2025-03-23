// SessionList.js
import React, { useEffect, useState } from 'react';
import { fetchSessions, deleteSession } from '../api';

const SessionList = ({ onSelectSession, onSessionDeleted, refreshTrigger }) => {
  const [sessions, setSessions] = useState([]);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const loadSessions = async () => {
    setIsLoading(true);
    try {
      const data = await fetchSessions();
      setSessions(data);
    } catch (error) {
      console.error('Error loading sessions:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Load sessions when component mounts or refreshTrigger changes
  useEffect(() => {
    loadSessions();
  }, [refreshTrigger]);

  const handleDelete = async (e, sessionId) => {
    e.stopPropagation(); // Prevent session selection when clicking delete
    if (window.confirm('Are you sure you want to delete this session?')) {
      setIsDeleting(true);
      try {
        await deleteSession(sessionId);
        loadSessions(); // Refresh the list
        if (onSessionDeleted) onSessionDeleted(sessionId);
      } catch (error) {
        console.error('Error deleting session:', error);
        alert('Failed to delete session');
      } finally {
        setIsDeleting(false);
      }
    }
  };

  return (
    <div style={{ width: '40%', border: '1px solid #ddd', padding: '15px', borderRadius: '10px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
        <h3 style={{ margin: 0 }}>Previous Sessions</h3>
        <button
          onClick={loadSessions}
          disabled={isLoading}
          style={{
            padding: '6px 12px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            opacity: isLoading ? 0.7 : 1,
            display: 'flex',
            alignItems: 'center',
            gap: '5px'
          }}
        >
          {isLoading ? '⌛' : '🔄'} {isLoading ? 'Loading...' : 'Refresh'}
        </button>
      </div>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {sessions.map(session => (
          <li 
            key={session.session_id} 
            style={{ 
              cursor: 'pointer', 
              marginBottom: '10px',
              padding: '8px',
              borderRadius: '5px',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              backgroundColor: '#f8f9fa',
              transition: 'background-color 0.2s'
            }}
            onMouseEnter={e => e.currentTarget.style.backgroundColor = '#e9ecef'}
            onMouseLeave={e => e.currentTarget.style.backgroundColor = '#f8f9fa'}
          >
            <div onClick={() => onSelectSession(session.session_id)}>
              📅 {new Date(session.test_date).toLocaleDateString()}
            </div>
            <button
              onClick={(e) => handleDelete(e, session.session_id)}
              disabled={isDeleting}
              style={{
                padding: '4px 8px',
                backgroundColor: '#dc3545',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                opacity: isDeleting ? 0.7 : 1
              }}
            >
              🗑️ Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SessionList;
