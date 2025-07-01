// Dashboard.jsx
import React, { useState } from 'react';
import './Dashboard.css';
import OptionPanel from './OptionPanel';
import ManualControl from './ManualControl';

function Dashboard() {
  const [manualMode, setManualMode] = useState(false);

  return (
    <div className="dashboard-container">
      <h2>📹 Dashboard</h2>

      <div className="video-container">
        <iframe
          src="http://192.168.1.101:8081/stream"
          title="Car Stream"
          allow="fullscreen"
        />
      </div>

      <OptionPanel manualMode={manualMode} setManualMode={setManualMode} />

      {manualMode && <ManualControl />}
    </div>
  );
}

export default Dashboard;
