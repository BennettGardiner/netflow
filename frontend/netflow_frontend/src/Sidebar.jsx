import React, { useEffect, useState } from 'react';
import './Sidebar.css';

const nodeTypes = [
  { label: 'Supply', value: 'supply', reactFlowType: 'input' },
  { label: 'Demand', value: 'demand', reactFlowType: 'output' },
  { label: 'Storage', value: 'storage', reactFlowType: 'default' }
];

function Sidebar({ onSolveClick }) {
  return (
    <aside>
      <div className="sidebar">
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
        <button className="solve-button" onClick={onSolveClick}>Solve</button>
      </div>
    </aside>
  );
};

export default Sidebar;