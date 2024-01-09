import React, { useState } from 'react';
import './Sidebar.css';

const nodeTypes = [
  { label: 'Supply', value: 'supply', reactFlowType: 'input' },
  { label: 'Demand', value: 'demand', reactFlowType: 'output' },
  { label: 'Storage', value: 'storage', reactFlowType: 'default' }
];

function Sidebar({ onSolveClick, onMaxTimestepsChange }) {
  const [timeSteps, setTimeSteps] = useState(0);

  const handleTimestepsChange = (event) => {
    const newValue = parseInt(event.target.value, 10);
    if (!isNaN(newValue)) {
      onMaxTimestepsChange(newValue);
    }
  };

  return (
    <aside>
      <div className="sidebar">
        <h3 className="app__title">NETFLOW</h3>
        <h3 className="app__subtitle">Network Flow Optimisation</h3>

        <h3 className="sidebar__title">Node Types</h3>
        
        <div className="sidebar__nodes">
          {nodeTypes.map((type) => (
            <div
              key={type.value}
              className={`sidebar__node sidebar__node--${type.value}`}
              onDragStart={(event) => event.dataTransfer.setData('application/reactflow', type.reactFlowType)}
              draggable
            >
              {type.label}
            </div>
          ))}
        </div>

        <div className="timesteps-section">
          <h4 className="timesteps-title">Timesteps</h4>
          <input
            type="number"
            className="timesteps-input"
            onChange={handleTimestepsChange}
            min="0"
          />
        </div>

        <button className="solve-button" onClick={onSolveClick}>Solve</button>
      </div>
    </aside>
  );
};

export default Sidebar;
