import { useCallback } from 'react';
import { Container, Row, Col } from "react-bootstrap";
import React from "react";
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
} from 'reactflow';

import 'reactflow/dist/style.css';

const initialNodes = [
  { id: '1', position: { x: 300, y: 100 }, data: { label: 'Ingenieria de Requisitos'}, style: {backgroundColor: '#6ede87'} },
  { id: '2', position: { x: 100, y: 300 }, data: { label: 'Calculo diferencial' } },
  { id: '3', position: { x: 700, y: 300 }, data: { label: 'Libre eleccion' }, style: { backgroundColor: '#ff0072'} },
];

const initialEdges = [{ id: 'e1-2', source: '1', target: '2'}, { id: 'e1-2', source: '1', target: '3' }];

export const Progress_graph = () => {

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const [anchorEl, setAnchorEl] = React.useState(null);

  const open = Boolean(anchorEl);
  const id = open ? "simple-popover" : undefined;

  const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  return (
    <section className="progress" id="progress">
        <Container>
            <div style={{ height: 400 }}>
                <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                onElementClick={(event, element) => {
                    console.log("click", element);
                    handleClick(event);
                  }}
                >
                <MiniMap />
                <Controls />
                <Background />
                </ReactFlow>
            </div>
        </Container>
    </section>
  )
}
