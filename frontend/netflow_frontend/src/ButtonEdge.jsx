import React from 'react';
import { getBezierPath, getMarkerEnd } from 'reactflow';

const ButtonEdge = ({
    id,
    sourceX,
    sourceY,
    targetX,
    targetY,
    sourcePosition,
    targetPosition,
    style = {},
    data,
    arrowHeadType,
    markerEndId,
}) => {
    const edgePath = getBezierPath({
        sourceX,
        sourceY,
        sourcePosition,
        targetX,
        targetY,
        targetPosition,
    });
    const markerEnd = getMarkerEnd(arrowHeadType, markerEndId);

    const costLabel = data && data.cost && data.cost !== 0 ? `Cost: ${data.cost}` : '';
    const capacityLabel = data && data.capacity ? `Capacity: ${data.capacity}` : '';

    const shouldRotateLabels = targetX < sourceX;

    // Calculate the midpoint of the handles
    const midpointX = (sourceX + targetX) / 2;
    const midpointY = (sourceY + targetY) / 2;

    // Calculate transform-origin based on the midpoint
    const transformOrigin = `${midpointX}px ${midpointY}px`;

    // Adjust startOffset based on rotation
    const startOffset = shouldRotateLabels ? "60%" : "40%";

    // Style for rotated labels
    const rotateStyle = shouldRotateLabels
        ? { transform: 'rotate(180deg)', transformOrigin: transformOrigin }
        : {};

    return (
        <>
            <path
                id={id}
                style={style}
                className="react-flow__edge-path"
                d={edgePath}
                markerEnd={markerEnd}
            />
            {costLabel && (
                <text style={rotateStyle}>
                    <textPath
                        href={`#${id}`}
                        startOffset={startOffset}
                        textAnchor="middle"
                        style={{ fontSize: '18px', fill: 'white' }}
                    >
                        <tspan dy="-0.75em">{costLabel}</tspan>
                    </textPath>
                </text>
            )}
            {capacityLabel && (
                <text style={rotateStyle}>
                    <textPath
                        href={`#${id}`}
                        startOffset={startOffset}
                        textAnchor="middle"
                        style={{ fontSize: '18px', fill: 'white' }}
                    >
                        <tspan dy="1.2em">{capacityLabel}</tspan>
                    </textPath>
                </text>
            )}
        </>
    );
};

export default ButtonEdge;
