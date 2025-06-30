// CarSelection.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './CarSelection.css';

const mockCars = [
  { name: 'Car A', ip: '192.168.1.101' },
  { name: 'Car B', ip: '192.168.1.102' }
];

function CarSelection() {
  const [cars, setCars] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    setTimeout(() => setCars(mockCars), 1000);
  }, []);

  const handleConnect = () => navigate('/dashboard');

  return (
    <div className="car-select">
      <h2>Select a Car</h2>
      {cars.length === 0 ? (
        <p>Searching...</p>
      ) : (
        cars.map((car, i) => (
          <div key={i} className="car-card">
            <p>{car.name} ({car.ip})</p>
            <button onClick={handleConnect}>Connect</button>
          </div>
        ))
      )}
    </div>
  );
}

export default CarSelection;
