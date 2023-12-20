export default function Modal({ isOpen, children, onClose }) {
  if (!isOpen) {
    return null;
  }

  return (
    <div style={customStyles.modal}>
      <div style={customStyles.overlay} onClick={onClose} />
      <div style={customStyles.content}>
        {children}
      </div>
    </div>
  );
}

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
  },
  overlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
  },
  content: {
    backgroundColor: '#fff',
    padding: '20px',
    maxWidth: '500px',
    margin: '0 auto',
    position: 'relative',
    overflow: 'auto',
    maxHeight: '80%',
    borderRadius: '10px',
  },
};
