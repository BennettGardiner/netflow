import React, { useEffect, useState } from 'react';
import './Sidebar.css';

const nodeTypes = ['supply', 'demand', 'storage'];

function Sidebar({ onSolveClick }) {
  return (
    <aside>
      <div className="sidebar">
        <h3 className="sidebar__title">Node Types</h3>
        <div className="sidebar__nodes">
          {nodeTypes.map((type) => (
            <div
              key={type}
              className={`sidebar__node sidebar__node--${type}`}
              onDragStart={(event) => event.dataTransfer.setData('application/reactflow', type)}
              draggable
            >
              {type.charAt(0).toUpperCase() + type.slice(1)}
            </div>
          ))}
        </div>
        <button className="solve-button" onClick={onSolveClick}>Solve</button>
      </div>
    </aside>
  );
};

export default Sidebar;