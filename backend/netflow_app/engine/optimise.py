import pulp as pl

def optimise_network(data):
    print("Optimising network using data")
    
    nodes = data['nodes']
    arcs = data['arcs']

    # todo: populate this from node supply data
    supplies = {
        's1': 4,
        's2': 5,
    } 

    # todo: populate this from node demand data
    demands = {
        'd1': 6,
        'd2': 3,
    } 

    # todo: populate this from arc connection data
    costs = {
        's1': {
            'd1': 2,
            'd2': 3,
        },
        's2': {
            'd1': 3,
            'd2': 2,
        },
    }

    print(f"Using nodes {[node['node_name'] for node in data['nodes']]}")
    
    for arc in arcs:
        start_node_name = [node['node_name'] for node in nodes if node['id']==arc['start_node']][0]
        end_node_name = [node['node_name'] for node in nodes if node['id']==arc['end_node']][0]
        print(f"Using arc from {start_node_name} to {end_node_name}")

    # Initialize the model
    model = pl.LpProblem("NetworkOptimization", pl.LpMinimize)

    # Decision variables for flow on each arc
    flow = {}
    for supply_node in supplies:
        for demand_node in demands:
            flow[supply_node, demand_node] = pl.LpVariable(f'flow_{supply_node}_{demand_node}', lowBound=0, cat='Continuous')

    # Supply constraints
    for supply_node in supplies:
        model += (
            pl.lpSum(flow[supply_node, demand_node] for demand_node in demands) <= supplies[supply_node], 
            f"SupplyConstraint_{supply_node}"
        )

    # Demand constraints
    for demand_node in demands:
        model += (
            pl.lpSum(flow[supply_node, demand_node] for supply_node in supplies) == demands[demand_node], 
            f"DemandConstraint_{demand_node}"
        )

    # Objective function: Minimize total cost
    total_cost = pl.lpSum(
        costs[supply_node][demand_node] * flow[supply_node, demand_node] 
        for supply_node in supplies 
        for demand_node in demands
    )
    model += total_cost

    # Solve the model
    model.solve()

    # Print the results
    if pl.LpStatus[model.status] == 'Optimal':
        print("Optimal value:", pl.value(model.objective))
        for supply_node in supplies:
            for demand_node in demands:
                print(f"Flow from {supply_node} to {demand_node}: {flow[supply_node, demand_node].varValue}")
    else:
        print("No optimal solution found.")

    return model.objective