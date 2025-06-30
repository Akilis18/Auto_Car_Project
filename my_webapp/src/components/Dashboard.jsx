// Dashboard.jsx
import React, { useState } from 'react';
import './Dashboard.css';
import OptionPanel from './OptionPanel';
import ManualControl from './ManualControl';

function Dashboard() {
  const [manualMode, setManualMode] = useState(false);

  return (
    <div className="dashboard">
      <h2>📹 Dashboard</h2>
      <iframe
        src="http://192.168.1.101:8081/stream"
        width="480"
        height="360"
        title="Car Stream"
      />
      <OptionPanel manualMode={manualMode} setManualMode={setManualMode} />
      {manualMode && <ManualControl />}
    </div>
  );
}

export default Dashboard;
