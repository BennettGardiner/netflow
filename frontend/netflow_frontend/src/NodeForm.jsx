import React, { useState } from 'react';
import Modal from './Modal';

function NodeForm({ isOpen, onRequestClose, onSubmit, nodeData }) { 
  const [nodeInfo, setNodeInfo] = useState({
    nodeLabel: '',
  });

  const handleChange = (event) => {
    setNodeInfo({ ...nodeInfo, [event.target.name]: event.target.value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(nodeInfo, nodeData);
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
        <button type="submit">Submit</button>
      </form>
    </Modal>
  );
}

export default NodeForm;
