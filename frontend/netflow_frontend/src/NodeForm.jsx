import React, { useState } from 'react';
import Modal from './Modal';

function NodeForm({ isOpen, onRequestClose, onSubmit }) {
  const [nodeInfo, setNodeInfo] = useState({
    nodeLabel: '',
    nodeType: '',
  });

  const handleChange = (event) => {
    setNodeInfo({ ...nodeInfo, [event.target.name]: event.target.value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(nodeInfo);
  };

  return (
    <Modal isOpen={isOpen} onClose={onRequestClose}>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <label>
            Node name:
            <input type="text" name="nodeLabel" onChange={handleChange} />
          </label>
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label>
            Node type:
            <select name="type" onChange={handleChange}>
              <option value="">Select...</option>
              <option value="supply">Supply</option>
              <option value="demand">Demand</option>
              <option value="storage">Storage</option>
              {/* Other options... */}
            </select>
          </label>
        </div>
        {/* Other fields... */}
        <button type="submit">Submit</button>
      </form>
    </Modal>
  );
}

export default NodeForm;
