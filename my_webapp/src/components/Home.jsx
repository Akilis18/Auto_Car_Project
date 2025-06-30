// Home.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <h1>🚗 Auto Car UI</h1>
      <p>Welcome! Click below to get started.</p>
      <button onClick={() => navigate('/select-car')}>Start</button>
    </div>
  );
}

export default Home;
