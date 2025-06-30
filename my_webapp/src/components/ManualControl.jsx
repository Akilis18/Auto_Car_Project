import React from 'react';
import { Joystick } from 'react-joystick-component';
import './ManualControl.css'

function ManualControl() {
  const handleMove = (event) => {
    console.log("Move:", event);
    // TODO: send direction/speed via WebSocket
  };

  const handleStop = () => {
    console.log("Joystick stopped");
    // TODO: send stop signal
  };

  return (
    <div className="manual-control">
        <h4>🕹 Manual Control Mode</h4>
        <div className="joystick-placeholder">
            <Joystick
                size={100}
                baseColor="gray"
                stickColor="black"
                move={handleMove}
                stop={handleStop}
            />
        </div>
    </div>
  );
}

export default ManualControl;
