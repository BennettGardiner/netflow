import pulp as pl

def optimise_network(data):
    print("Optimising network using data")
    
    nodes = data['nodes']
    arcs = data['arcs']

    # todo: replace these with supplies and demands from the data. Will need to alter the Node model to include supply/demand
    # Supply Dictionary
    supplies = {node['node_name']: 1 for node in nodes if node['type'] == 'supply'}

    # Demand Dictionary
    demands = {node['node_name']: 1 for node in nodes if node['type'] == 'demand'}

    # Costs Dictionary
    costs = {supply['node_name']: {} for supply in nodes if supply['type'] == 'supply'}
    for arc in arcs:
        supply_name = next(node['node_name'] for node in nodes if node['id'] == arc['start_node'])
        demand_name = next(node['node_name'] for node in nodes if node['id'] == arc['end_node'])
        costs[supply_name][demand_name] = arc['cost']

    print("Supplies:", supplies)
    print("Demands:", demands)
    print("Costs:", costs)

    print(f"Using nodes {[node['node_name'] for node in nodes]}")
    
    for arc in arcs:
        start_node_name = [node['node_name'] for node in nodes if node['id']==arc['start_node']][0]
        end_node_name = [node['node_name'] for node in nodes if node['id']==arc['end_node']][0]
        print(f"Using arc from {start_node_name} to {end_node_name} with cost {arc['cost']}")

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

    # todo: implement a real node balance equilibrium constraint

    # Objective function: Minimize total cost
    total_cost = pl.lpSum(
        costs[supply_node].get(demand_node, 1e6) * flow[supply_node, demand_node]  # todo: only sum over existing arcs
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
                flow_val = flow[supply_node, demand_node].varValue
                if flow_val == 1:
                    print(f"Flow from {supply_node} to {demand_node} at cost {costs[supply_node][demand_node]}: {flow_val}")
    else:
        print("No optimal solution found.")

    return model.objective