
from netflow_app.engine.optimise import optimise_network
from netflow_app.engine.preprocess import create_engine_data


def solve_network_flow(data):
    
    print("Solving network flow problem...")
    supply_nodes, demand_nodes, storage_nodes, engine_nodes, engine_arcs, timesteps = create_engine_data(data)
    
    engine_data = {
        'parameters': {
            'timesteps': timesteps
        },
        'supply_nodes': supply_nodes,
        'demand_nodes': demand_nodes,
        'storage_nodes': storage_nodes,
        'arcs': engine_arcs
    }
    return optimise_network(engine_data)