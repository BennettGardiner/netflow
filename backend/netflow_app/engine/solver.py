
from netflow_app.engine.optimise import optimise_network


def solve_network_flow(data):
    
    print("Solving network flow problem...")
    print(optimise_network(data))