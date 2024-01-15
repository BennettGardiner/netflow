from pydantic import BaseModel
from typing import List, Dict, Optional

class EngineNode(BaseModel):
    id: str
    timestep: int

class EngineSupplyNode(EngineNode):
    supply_amount: float


class EngineDemandNode(EngineNode):
    demand_amount: float


class EngineStorageNode(EngineNode):
    initial_amount: float


class EngineArc(BaseModel):
    id: int
    start_engine_node: EngineNode
    end_engine_node: EngineNode
    cost: float
    capacity: Optional[float]

def create_engine_supply_nodes(nodes, timesteps):
    engine_nodes = []
    for node in nodes:
        for timestep in range(timesteps):
            engine_node_id = f"{node['node_name']}_{timestep}"
            supply_amount = node['supply_amount'] if timestep == 0 else 0
            engine_nodes.append(EngineSupplyNode(id=engine_node_id, timestep=timestep, supply_amount=supply_amount))
    return engine_nodes

def create_engine_demand_nodes(nodes, timesteps):
    engine_nodes = []
    for node in nodes:
        for timestep in range(timesteps):
            engine_node_id = f"{node['node_name']}_{timestep}"
            demand_amount = node['demand_amount'] if timestep == 0 else 0
            engine_nodes.append(EngineDemandNode(id=engine_node_id, timestep=timestep, demand_amount=demand_amount))
    return engine_nodes

def create_engine_storage_nodes(nodes, timesteps):
    engine_nodes = []
    for node in nodes:
        for timestep in range(timesteps):
            engine_node_id = f"{node['node_name']}_{timestep}"
            initial_amount = node['initial_amount'] if timestep == 0 else 0
            engine_nodes.append(EngineStorageNode(id=engine_node_id, timestep=timestep, initial_amount=initial_amount))
    return engine_nodes

def create_engine_arcs(engine_nodes: List[EngineNode], arcs, timesteps):
    engine_arcs = []
    # Update the node_dict to use string IDs as keys
    node_dict = {node.id: node for node in engine_nodes}
    
    for arc in arcs:
        duration = arc['duration']
        for timestep in range(timesteps - duration):
            start_engine_node_id = f"{arc['start_node']}_{timestep}"
            end_engine_node_id = f"{arc['end_node']}_{timestep + duration}"
            start_engine_node = node_dict.get(start_engine_node_id)
            end_engine_node = node_dict.get(end_engine_node_id)

            if start_engine_node and end_engine_node:
                engine_arcs.append(
                    EngineArc(
                        id=arc['id'],
                        start_engine_node=start_engine_node, 
                        end_engine_node=end_engine_node, 
                        cost=arc['cost'], 
                        capacity=arc['capacity'])
                    )
    return engine_arcs

def create_engine_data(data):

    timesteps = data['parameters']['timesteps']

    supply_nodes = create_engine_supply_nodes(data['supply_nodes'], timesteps)
    demand_nodes = create_engine_demand_nodes(data['demand_nodes'], timesteps)
    storage_nodes = create_engine_storage_nodes(data['storage_nodes'], timesteps)
    engine_nodes = supply_nodes + demand_nodes + storage_nodes

    engine_arcs = create_engine_arcs(engine_nodes, data['arcs'], timesteps)

    return supply_nodes, demand_nodes, storage_nodes, engine_nodes, engine_arcs, timesteps