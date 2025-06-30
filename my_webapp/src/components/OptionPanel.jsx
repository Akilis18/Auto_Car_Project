// OptionPanel.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './OptionPanel.css';

function OptionPanel({ manualMode, setManualMode }) {
  const navigate = useNavigate();

  const toggleMode = () => setManualMode(!manualMode);
  const stopCar = () => navigate('/');

  return (
    <div className="options">
      <button onClick={toggleMode}>
        {manualMode ? 'Switch to Auto Mode' : 'Switch to Manual Mode'}
      </button>
      <button>Switch Camera View</button>
      <button onClick={stopCar}>Stop Car</button>
    </div>
  );
}

export default OptionPanel;
