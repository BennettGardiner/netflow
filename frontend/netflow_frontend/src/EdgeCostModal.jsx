import React, { useState } from 'react'; // Ensure useState is imported

const EdgeCostModal = ({ isOpen, onRequestClose, onSubmit }) => {
    const [cost, setCost] = useState('');

    if (!isOpen) return null;

    return (
        <div style={customStyles.modal}>
            <div style={customStyles.overlay} onClick={onRequestClose} />
            <div style={customStyles.content}>
                <h2>Set Edge Cost</h2>
                <input
                    type="number"
                    value={cost}
                    onChange={(e) => setCost(e.target.value)}
                    placeholder="Enter cost"
                    style={customStyles.input}
                />
                <button onClick={() => onSubmit(cost)} style={customStyles.button}>Submit</button>
                <button onClick={onRequestClose} style={customStyles.button}>Cancel</button>
            </div>
        </div>
    );
};

const customStyles = {
    modal: {
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000, // Ensure modal is on top
    },
    overlay: {
        position: 'absolute', // Change to 'absolute'
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundColor: 'rgba(0, 0, 0, 0.7)',
        zIndex: -1, // Push overlay behind the content
    },
    content: {
        position: 'relative', // Ensure this is positioned relative to the modal
        backgroundColor: '#fff',
        padding: '20px',
        maxWidth: '500px',
        borderRadius: '10px',
        zIndex: 1001, // Ensure content is above the overlay
    },
    input: {
        width: '26%',
        padding: '10px',
        marginBottom: '20px',
    },
    button: {
        marginRight: '10px',
        padding: '10px 20px',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
    },
};

export default EdgeCostModal;