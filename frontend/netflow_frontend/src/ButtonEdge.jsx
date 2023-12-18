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

    const label = data && data.label ? data.label : '';

    return (
        <>
            <path
                id={id}
                style={style}
                className="react-flow__edge-path"
                d={edgePath}
                markerEnd={markerEnd}
            />
            {label && (
                <text>
                    <textPath
                        href={`#${id}`}
                        startOffset="50%"
                        textAnchor="middle"
                        style={{ fontSize: '12px', fill: 'white' }}
                    >
                        {/* Empty tspan for buffer */}
                        <tspan dy="-0.4em" x="0"></tspan> 
                        {/* Actual label */}
                        <tspan dy="-0.4em" x="0">{label}</tspan>
                    </textPath>
                </text>
            )}
        </>
    );
};

export default ButtonEdge;
