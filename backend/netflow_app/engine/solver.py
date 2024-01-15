
# from netflow_app.engine.optimiser import optimise_network
from netflow_app.engine.preprocess import create_engine_data


def solve_network_flow(data):
    
    print("Solving network flow problem...")
    supply_nodes, demand_nodes, storage_nodes, engine_nodes, engine_arcs, timesteps = create_engine_data(data)
    import pdb; pdb.set_trace()
    # return optimise_network(data)