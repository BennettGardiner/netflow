import React, { useCallback, useState, useEffect } from 'react';
import ReactFlow, {
  useNodesState,
  useEdgesState,
  ReactFlowProvider,
  MiniMap,
  Controls,
  Background,
  addEdge,
  ConnectionMode,
  Handle,
  useOnSelectionChange,
} from 'reactflow';
import axios from 'axios';

import EdgeModal from './EdgeModal';
import Sidebar from './Sidebar';
import NodeForm from './NodeForm';
import './dark_theme.css';
import './error_modal.css';
import './colours.css';
import 'reactflow/dist/style.css';

import ButtonEdge from './ButtonEdge';

const initialNodes = [];
const initialEdges = [];

const minimapNodeColor = (node) => {
  switch (node.data.type) {
    case 'supply':
      return 'green';
    case 'demand':
      return 'red';
    case 'storage':
      return 'blue';
    default:
      return 'gray';
  }
};

const nodeColor = (type) => {
  switch (type) {
    case 'supply':
      return 'var(--supply-green)';
    case 'demand':
      return 'var(--demand-red)';
    case 'storage':
      return 'var(--storage-blue)';
    default:
      return 'var(--default-color)';
  }
};

const NodeContent = ({ data, type }) => {
  const horizontalPadding = '10px';
  const verticalPadding = '25px';

  return (
    <div style={{ 
      padding: `${verticalPadding} ${horizontalPadding}`, 
      border: '1px solid black', 
      backgroundColor: nodeColor(type), 
      color: 'white',
      position: 'relative',
    }}>
      {data.label}
      {data.amount !== undefined && (
        <div style={{ 
          position: 'absolute', 
          bottom: '10px', 
          right: '10px', 
          fontSize: '12px' 
        }}>
          {data.amount}
        </div>
      )}
    </div>
  );
};

const SupplyNode = ({ data }) => (
  <div>
    <Handle type="source" position="right" style={{ borderRadius: 0 }} />
    <NodeContent data={data} type="supply" />
  </div>
);

const DemandNode = ({ data }) => (
  <div>
    <Handle type="target" position="left" style={{ borderRadius: 0 }} />
    <NodeContent data={data} type="demand" /> 
  </div>
);

const StorageNode = ({ data }) => (
  <div>
    <Handle type="target" position="left" style={{ borderRadius: 0 }} />
    <NodeContent data={data} type="storage" />
    <Handle type="source" position="right" style={{ borderRadius: 0 }} />
  </div>
);

const nodeTypes = {
  input: SupplyNode,
  output: DemandNode,
  default: StorageNode,
};

const edgeTypes = {
  buttonedge: ButtonEdge, 
};

export default function App() {


  const [arcIdMap, setArcIdMap] = useState({}); // Map arc ids to edge ids

  const [isErrorModalOpen, setIsErrorModalOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const [selectedElement, setSelectedElement] = useState(null);

  // todo: make these way more robust 
  const isEdge = (element) => 'source' in element;
  const isNode = (element) => !('source' in element);

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [nodeData, setNodeData] = useState(null); 

  // Function to handle selection change in React Flow
  const onSelectionChange = useCallback(({ nodes, edges }) => {
    const selected = nodes[0] || edges[0];
    setSelectedElement(selected);
    if (selected) {
      console.log('Current selected element:', selected);
    }
  }, []);

   // Function to delete an element from the backend
   const deleteElement = async (element) => {
    let url;
    if (isNode(element)) {
      url = `http://127.0.0.1:8000/api/base-nodes/${element.data.label}/`;
    } else if (isEdge(element)) {
      const backendId = arcIdMap[element.id]; // Retrieve the backend ID
      if (!backendId) {
        console.log('arcIdMap:', arcIdMap)
        console.error('No backend ID found for edge:', element.id);
        return;
      }
      url = `http://127.0.0.1:8000/api/arcs/${backendId}/`;
    } else {
      console.error('Unrecognized element type:', element);
      return;
    }
  
    try {
      await axios.delete(url);
      console.log(`Deleted ${isNode(element) ? 'node' : 'arc'} with id ${element.id}`);
    } catch (error) {
      console.error('Error deleting element:', error);
    }
  };
  

  const handleKeyDown = useCallback(async (event) => {
    console.log('Key pressed:', event.key); // Debugging log
    console.log('event.key:', event.key);
    if (selectedElement) {
      console.log('Current selected element:', selectedElement);
    }
    if ((event.key === 'Backspace' || event.key === 'Delete') && selectedElement) {
      console.log('Trying to delete element:', selectedElement);
      await deleteElement(selectedElement);
        if (isNode(selectedElement)) {
            setNodes((nds) => nds.filter((n) => n.id !== selectedElement.id));
        } else if (isEdge(selectedElement)) {
            setEdges((eds) => eds.filter((e) => e.id !== selectedElement.id));
        }
        setSelectedElement(null); // Clear selection
    }
  }, [selectedElement, deleteElement, setNodes, setEdges]);

  useEffect(() => {
      document.addEventListener('keydown', handleKeyDown);
      return () => {
          document.removeEventListener('keydown', handleKeyDown);
      };
  }, [handleKeyDown]);


  
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

    setNodeData({ type: nodeType, position: position, });
    setIsModalOpen(true);
  }, []);

  const handleRequestClose = () => {
    setIsModalOpen(false); // Close the modal when requested.
  };

  const [isEdgeCostModalOpen, setIsEdgeCostModalOpen] = useState(false);
  const [newEdgeData, setNewEdgeData] = useState(null); // To temporarily store new edge data

  const handleEdgeSubmission = (cost, capacity) => {
    if (newEdgeData) {
        const edgeWithCost = { 
            ...newEdgeData, 
            data: { label: `${cost ? `Cost: ${cost}` : ''}${capacity ? `  Capacity: ${capacity}` : ''}` }
        };

        setEdges((eds) => addEdge(edgeWithCost, eds));

        console.log('Edge created from', newEdgeData.source, 'to', newEdgeData.target, 'with cost', cost, 'and capacity', capacity);
        const newEdgeForPost = {
            start_node: newEdgeData.source,
            end_node: newEdgeData.target,
            cost: cost ? parseFloat(cost) : 0,
            capacity: parseFloat(capacity)
        };

        const frontendEdgeId = `reactflow__edge-${newEdgeData.source}-${newEdgeData.target}`;

        // Make a POST request to backend with the edge data including cost
        fetch('http://127.0.0.1:8000/api/arcs/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newEdgeForPost),
        })
        .then((response) => response.json())
        .then((data) => {
            console.log('Arc', edgeWithCost, 'created with cost:', data.cost, 'and capacity:', data.capacity);
            setArcIdMap((prevMap) => ({ ...prevMap, [frontendEdgeId]: data.id  }));
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
};

  const onConnect = useCallback((params) => {
    setNewEdgeData({
      source: params.source,
      target: params.target,
      type: 'buttonedge', // Specify the custom edge type here
      animated: true
    });
    // Open modal to input cost
    setIsEdgeCostModalOpen(true);
  }, [setEdges]);

  const handleSubmit = (nodeInfo, nodeData) => {
    let apiEndpoint;
    let newNodeData = {
      node_name: nodeInfo.nodeLabel, // Only the name for backend
    };
  
    switch (nodeData.type) {
      case 'input':
        apiEndpoint = 'http://127.0.0.1:8000/api/supply-nodes/';
        newNodeData['supply_amount'] = parseFloat(nodeInfo.amount);
        break;
      case 'output':
        apiEndpoint = 'http://127.0.0.1:8000/api/demand-nodes/';
        newNodeData['demand_amount'] = parseFloat(nodeInfo.amount);
        break;
      case 'default':
        apiEndpoint = 'http://127.0.0.1:8000/api/storage-nodes/';
        break;
      default:
        console.error('Unsupported node type');
        return;
    }
  
    fetch(apiEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newNodeData),
    })
    .then(async (response) => {
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.node_name || 'Failed to create node');
      }
      return response.json();
    })
    .then((data) => {
        console.log('Node created:', data);
        const amount = nodeData.type === 'input' ? data.supply_amount : data.demand_amount;
        let newNodeType;
          switch (nodeData.type) {
            case 'input':
              newNodeType = 'supply';
              break;
            case 'output':
              newNodeType = 'demand';
              break;
            case 'default':
              newNodeType = 'storage';
              break;
            default:
              console.error('Unsupported node type:', nodeData.type);
              return;
          }
        const newNode = {
          id: nodeInfo.nodeLabel,
          type: nodeData.type,
          data: { 
            label: nodeInfo.nodeLabel,
            amount: amount,
            type: newNodeType // Add this to use in NodeContent for color
          },
          position: nodeData.position,
          style: {
            backgroundColor: nodeColor({ type: nodeData.type }),
            color: 'white',
            fontSize: '22px',
          },
        };
        setNodes((ns) => ns.concat(newNode));
      })
      .catch((error) => {
        setErrorMessage(error.message);
        setIsErrorModalOpen(true);
      });
      setIsModalOpen(false);
    };

  // Add this state to track if solution details should be displayed
  const [showSolutionDetails, setShowSolutionDetails] = useState(false);

  const [latestSolution, setLatestSolution] = useState(null);

  const fetchLatestSolution = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/solutions/');
      const solutions = response.data;
      if (solutions.length > 0) {
        const latestSolution = solutions[solutions.length - 1]; // Get the last solution
        setLatestSolution(latestSolution);
      }
    } catch (error) {
      console.error('Error fetching solutions:', error);
    }
  };
  
  const [edgesUpdated, setEdgesUpdated] = useState(false);
  useEffect(() => {
    if (latestSolution && latestSolution.arc_flows) {
      const updatedEdges = edges.map(edge => {
        // Check if the edge is part of the latest solution using arc_flows
        const isPartOfSolution = Object.values(latestSolution.arc_flows).some(arcFlow => 
          arcFlow.arc.start_node === edge.source && arcFlow.arc.end_node === edge.target
        );
  
        if (isPartOfSolution) {
          // Update the style for highlighting
          // todo: base the stroke width on the flow amount compared to the overall amount in the network
          return { ...edge, style: { stroke: 'green', strokeWidth: 6, zlevel: 100 } };
        } else {
          // Reset style for non-solution edges
          return { ...edge, style: { stroke: 'black', strokeWidth: 2 } };
        }
      });
  
      // Update the edges state with the new array
      setEdges(updatedEdges);
    }
  }, [latestSolution, edges]);  
  
  // Reset edgesUpdated when latestSolution changes
  useEffect(() => {
    setEdgesUpdated(true);
  }, [latestSolution]);

  const handleShowSolutionDetails = () => {
    setShowSolutionDetails(!showSolutionDetails);
  };
  
  
  const handleSolveClick = useCallback(async () => {
    try {
      await axios.post('http://127.0.0.1:8000/api/solve/');
      await fetchLatestSolution(); // Fetch the latest solution after solving
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
          onSelectionChange={onSelectionChange}
          onDrop={onDrop}
          onDragOver={onDragOver}
          onConnect={onConnect}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          edgeTypes={edgeTypes}
          nodeTypes={nodeTypes}
          connectionMode={ConnectionMode.Loose}
          >
            <MiniMap nodeColor={minimapNodeColor} pannable={true}/>
            <Controls />
            <Background color="#aaa" gap={16} />
          </ReactFlow>
          
        </ReactFlowProvider>
        <NodeForm
          isOpen={isModalOpen}
          onRequestClose={handleRequestClose}
          onSubmit={handleSubmit}
          nodeData={nodeData}
        />
      </div>
      <button 
        onClick={handleShowSolutionDetails}
        style={{ 
          fontSize: 18,
          fontWeight: 'bold', 
          whiteSpace: 'pre-line' // This will allow for line breaks
        }}
      >
        {showSolutionDetails ? 'Hide\nSolution\nDetails' : 'Show\nSolution\nDetails'}
      </button>

    {showSolutionDetails && latestSolution && (
      <div>
        <h3>Solution Details:</h3>
        <p>Total Cost: {latestSolution.total_cost}</p>
        <p>Utilized Arcs:</p>
        <ul>
          {Object.entries(latestSolution.arc_flows).map(([arcId, arcData]) => (
            <li key={arcId}>
              Arc {arcId}: Flow of {arcData.flow} from Node {arcData.arc.start_node} to Node {arcData.arc.end_node}, Cost: {arcData.arc.cost} x {arcData.flow} = {arcData.arc.cost * arcData.flow}
            </li>
          ))}
        </ul>
      </div>
    )}
    {isErrorModalOpen && (
      <div className="error-modal">
        <p>Error: {errorMessage}</p>
        <button onClick={() => setIsErrorModalOpen(false)}>Close</button>
      </div>
    )}
      {isEdgeCostModalOpen && (
            <EdgeModal 
                isOpen={isEdgeCostModalOpen}
                onRequestClose={() => setIsEdgeCostModalOpen(false)}
                onSubmit={(cost, capacity) => {
                    setIsEdgeCostModalOpen(false);
                    handleEdgeSubmission(cost, capacity);
                }}
            />
        )}
    </div>
  );
}
