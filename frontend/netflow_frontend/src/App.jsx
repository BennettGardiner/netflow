// App.jsx
import React, { useCallback, useState } from 'react';
import ReactFlow, {
  useNodesState,
  useEdgesState,
  ReactFlowProvider,
  MiniMap,
  Controls,
  Background,
  addEdge,
} from 'reactflow';
import Sidebar from './Sidebar';
import NodeForm from './NodeForm';
import './colours.css';

import 'reactflow/dist/style.css';

const initialNodes = [];
const initialEdges = [];

const nodeColor = (node) => {
  switch (node.type) {
    case 'supply':
      return 'var(--supply-green)';
    case 'storage':
      return 'var(--storage-blue)';
    case 'demand':
      return 'var(--demand-red)';
    default:
      return 'var(--default-color)';
  }
};

export default function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [nodeData, setNodeData] = useState(null); // Initialize nodeData as null

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback((event) => {
    event.preventDefault();

    const reactFlowBounds = document.querySelector('.react-flow__renderer').getBoundingClientRect();
    const nodeType = event.dataTransfer.getData('application/reactflow');
    const position = {
      x: event.clientX - reactFlowBounds.left,
      y: event.clientY - reactFlowBounds.top,
    };

    setNodeData({ type: nodeType, position: position }); // Set nodeData
    setIsModalOpen(true);
  }, []);

  const handleRequestClose = () => {
    setIsModalOpen(false); // Close the modal when requested.
  };

  const onConnect = useCallback((params) => {
    const newEdge = {
      source: params.source,
      target: params.target,
      type: 'step',
      animated: true,
    };
    setEdges((edges) => addEdge(newEdge, edges));
  }, [setEdges]);

  return (
    <div style={{ height: '100vh', display: 'flex' }}>
      <Sidebar />
      <div style={{ flex: 1, position: 'relative' }} onDragOver={onDragOver} onDrop={onDrop}>
        <ReactFlowProvider>
          <ReactFlow nodes={nodes} edges={edges} onConnect={onConnect}>
            <MiniMap nodeColor={nodeColor} />
            <Controls />
            <Background color="#aaa" gap={16} />
          </ReactFlow>
        </ReactFlowProvider>
        <NodeForm
          isOpen={isModalOpen}
          onRequestClose={handleRequestClose}
          onSubmit={(nodeInfo) => {
            // Here, we're making a POST request to create a new node,
            // then adding the new node to our state.
            fetch('http://localhost:8000/api/nodes/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(nodeInfo),
            })
              .then((response) => response.json())
              .then((data) => {
                console.log('Node created:', data);
                const newNode = {
                  id: data.id.toString(),
                  type: nodeData.type, // Use nodeData
                  position: nodeData.position, // Use nodeData
                  data: { label: `${nodeInfo.nodeLabel}` },
                  style: {
                    backgroundColor:
                      nodeData.type === 'supply'
                        ? 'var(--supply-green)'
                        : nodeData.type === 'demand'
                        ? 'var(--demand-red)'
                        : nodeData.type === 'storage'
                        ? 'var(--storage-blue)'
                        : 'var(--default-color)', // default color
                  },
                };
                setNodes((ns) => ns.concat(newNode));
              })
              .catch((error) => {
                console.error('Error:', error);
              });
            setIsModalOpen(false);
          }}
        />
      </div>
    </div>
  );
}
