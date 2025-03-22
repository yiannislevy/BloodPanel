// Dashboard.js
import React, { useState } from 'react';
import Upload from './Upload';
import SessionList from './SessionList';
import SessionDetails from './SessionDetails';

const Dashboard = () => {
  const [selectedSessionId, setSelectedSessionId] = useState(null);

  const handleUpload = () => {
    setSelectedSessionId(null); // refresh list after upload
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: 'auto' }}>
      <h1 style={{ textAlign: 'center' }}>Blood Test Dashboard</h1>
      <Upload onFileUpload={handleUpload} />
      <div style={{ display: 'flex', gap: '20px', marginTop: '40px' }}>
        <SessionList onSelectSession={setSelectedSessionId} />
        {selectedSessionId && <SessionDetails sessionId={selectedSessionId} />}
      </div>
    </div>
  );
};

export default Dashboard;
