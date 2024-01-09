import React, { useState, useEffect } from 'react';
import Modal from './Modal';

function NodeForm({ isOpen, onRequestClose, onSubmit, nodeData }) {
  const initialState = {
    nodeLabel: '',
    amount: 0
  };

  const [nodeInfo, setNodeInfo] = useState(initialState);
  const [initialAmount, setInitialAmount] = useState(0);

  useEffect(() => {
    if (isOpen) {
      setNodeInfo(initialState); // Reset state when the modal is opened
    }
  }, [isOpen]); // Dependency array includes isOpen

  useEffect(() => {
    if (isOpen) {
      setNodeInfo(initialState);
      setInitialAmount(0); // Reset the initial amount
    }
  }, [isOpen]);

  const handleClose = () => {
      setNodeInfo(initialState); // Reset the form state
      onRequestClose(); // Call the original close handler
  };

  const handleChange = (event) => {
    setNodeInfo({ ...nodeInfo, [event.target.name]: event.target.value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const nodeSubmissionInfo = { ...nodeInfo };
    if (nodeData && nodeData.type === 'default') {
      nodeSubmissionInfo.initialAmount = parseFloat(initialAmount);
    }
    onSubmit(nodeSubmissionInfo, nodeData);
  setNodeInfo(initialState);
    setInitialAmount(0);
  };

  const renderAmountField = () => {
    if (nodeData) {
      if (nodeData.type === 'input') {
        return (
            <div style={{ marginBottom: '10px' }}>
                <label>
                    Supply amount:
                    <input 
                        type="number" 
                        name="amount" 
                        value={nodeInfo.amount} 
                        onChange={handleChange} 
                    />
                </label>
            </div>
          );
        }
      else if (nodeData.type === 'output') {
          return (
              <div style={{ marginBottom: '10px' }}>
                  <label>
                      Demand amount:
                      <input 
                          type="number" 
                          name="amount" 
                          value={nodeInfo.amount} 
                          onChange={handleChange} 
                      />
                  </label>
              </div>
          );
      }
      else if (nodeData.type === 'default') { // For storage nodes
        return (
          <div style={{ marginBottom: '10px' }}>
            <label>
              Initial amount:
              <input 
                type="number"
                name="initialAmount"
                value={initialAmount}
                onChange={(e) => setInitialAmount(e.target.value)}
              />
            </label>
          </div>
        );
      }
    }
    return null;
};
  
  return (
    <Modal isOpen={isOpen} onClose={handleClose}>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
            <label>
                Node name:
                <input 
                    type="text" 
                    name="nodeLabel" 
                    value={nodeInfo.nodeLabel} 
                    onChange={handleChange} 
                />
            </label>
        </div>
        {renderAmountField()}
        <button type="submit">Submit</button>
      </form>
    </Modal>
  );
}

export default NodeForm;
