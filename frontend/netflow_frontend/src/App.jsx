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
import axios from 'axios';

import Sidebar from './Sidebar';
import NodeForm from './NodeForm';
import './colours.css';

import 'reactflow/dist/style.css';

const initialNodes = [];
const initialEdges = [];

const nodeTypeMapping = {
  input: 'supply',
  output: 'demand',
  default: 'storage',
};
const nodeColor = (node) => {
  switch (node.type) {
    case 'input':
      return 'var(--supply-green)';
    case 'default':
      return 'var(--storage-blue)';
    case 'output':
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

    setNodeData({ type: nodeType, position: position, }); // Set nodeData
    setIsModalOpen(true);
  }, []);

  const handleRequestClose = () => {
    setIsModalOpen(false); // Close the modal when requested.
  };

  const onConnect = useCallback((params) => {
    const newArc = {
        start_node: params.source,
        end_node: params.target,
    };
    console.log(newArc);
    fetch('http://127.0.0.1:8000/api/arcs/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(newArc),
    })
    .then((response) => response.json())
    .then((data) => {
        console.log('Arc created:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
        console.log(params.source)
        console.log(params.target.id)
    });
    const newEdge = {
      source: params.source,
      target: params.target,
      type: 'bezier',
      animated: true,
    };
    setEdges((edges) => addEdge(newEdge, edges));
  }, [setEdges]);
  
  const handleSubmit = (nodeInfo, nodeData) => {
    // Here, we're making a POST request to create a new node,
    // then adding the new node to our state.
    const newNodeData = {
      ...nodeData,
      type: nodeTypeMapping[nodeData.type], // Use mapped type
      node_name: nodeInfo.nodeLabel, 
    };
    fetch('http://127.0.0.1:8000/api/nodes/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newNodeData),
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((err) => {
            throw err; // Throw the error if response is not ok
          });
        }
        return response.json();
      })
      .then((data) => {
        console.log('Node created:', data);
        const newNode = {
          id: data.id.toString(),
          type: nodeData ? nodeData.type : '', // Use nodeData if available, otherwise use an empty string
          position: nodeData ? nodeData.position : null, // Use nodeData if available, otherwise use null
          data: { label: `${nodeInfo.nodeLabel}` },
          style: {
            backgroundColor:
            newNodeData.type === 'supply'
              ? 'var(--supply-green)'
              : newNodeData.type === 'demand'
              ? 'var(--demand-red)'
              : newNodeData.type === 'storage'
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
  };

  const handleSolveClick = useCallback(async () => {
    try {
      await axios.post('http://127.0.0.1:8000/api/solve/');
    } catch (error) {
      console.error('An error occurred while sending data to the engine:', error);
    }
  }, []);

  return (
    <div style={{ height: '100vh', display: 'flex' }}>
      <Sidebar onSolveClick={handleSolveClick} />
      <div style={{ flex: 1, position: 'relative' }} onDragOver={onDragOver} onDrop={onDrop} >
        <ReactFlowProvider>
          <ReactFlow 
          nodes={nodes} 
          edges={edges} 
          onDrop={onDrop}
          onDragOver={onDragOver}
          onConnect={onConnect}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          >
            <MiniMap nodeColor={nodeColor} pannable={true}/>
            <Controls />
            <Background color="#aaa" gap={16} />
          </ReactFlow>
        </ReactFlowProvider>
        <NodeForm
          isOpen={isModalOpen}
          onRequestClose={handleRequestClose}
          onSubmit={handleSubmit}
          nodeData={nodeData} // Add this line
        />
      </div>
    </div>
  );
}
