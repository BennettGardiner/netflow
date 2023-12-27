import pulp as pl

def optimise_network(data):
    print("Optimising network using data")
    
    supply_nodes = data['supply_nodes']
    demand_nodes = data['demand_nodes']
    arcs = data['arcs']

    # Handling the UUIDs as strings
    # todo: Put this on the viewset / serializer as appropriate
    for arc in arcs:
        arc['start_node'] = str(arc['start_node'])
        arc['end_node'] = str(arc['end_node'])

    # Initialize the model
    model = pl.LpProblem("NetworkOptimization", pl.LpMinimize)

    # Decision variables for flow on each arc
    flow = {}
    for supply in supply_nodes:
        for demand in demand_nodes:
            flow[supply['id'], demand['id']] = pl.LpVariable(f'flow_{supply["id"]}_{demand["id"]}', lowBound=0, cat='Continuous')

    # Supply constraints
    for supply in supply_nodes:
        model += (
            pl.lpSum(flow[supply['id'], demand['id']] for demand in demand_nodes) <= supply['supply_amount'], 
            f"SupplyConstraint_{supply['id']}"
        )

    # Demand constraints
    for demand in demand_nodes:
        model += (
            pl.lpSum(flow[supply['id'], demand['id']] for supply in supply_nodes) == demand['demand_amount'], 
            f"DemandConstraint_{demand}"
        )

    # todo: implement a real node balance equilibrium constraint

    # Objective function: Minimize total cost
    total_cost = pl.lpSum(
        arc['cost'] * flow[arc['start_node'], arc['end_node']]  
        for arc in arcs
    )
    model += total_cost

    # Solve the model
    model.solve()

    # Print the results
    if pl.LpStatus[model.status] == 'Optimal':
        print("Optimal value:", pl.value(model.objective))
        for arc in arcs:
            flow_val = flow[arc['start_node'], arc['end_node']].varValue
            if flow_val == 1:
                print(f"Flow from {arc['start_node']} to {arc['end_node']}: {flow_val}")
    else:
        print("No optimal solution found.")

    return model.objective