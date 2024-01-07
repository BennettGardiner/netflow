from django.utils import timezone
import pulp as pl

from netflow_app.models import Solution

def optimise_network(data):
    print("Optimising network using data")
    
    supply_nodes = data['supply_nodes']
    demand_nodes = data['demand_nodes']
    storage_nodes = data['storage_nodes']
    arcs = data['arcs']

    # Initialize the model
    model = pl.LpProblem("NetworkOptimization", pl.LpMinimize)

    # Decision variables for flow on each arc
    flow = {}
    for arc in arcs:
        start_node = arc['start_node']
        end_node = arc['end_node']
        flow[start_node, end_node] = pl.LpVariable(f'flow_{start_node}_{end_node}', lowBound=0, cat='Continuous')
        
    # Supply constraints
    for supply in supply_nodes:
        supply_node_name = supply['node_name']
        supply_amount = supply['supply_amount']
        model += (
            pl.lpSum(flow[supply_node_name, arc['end_node']] for arc in arcs if arc['start_node'] == supply_node_name) <= supply_amount, 
            f"SupplyConstraint_{supply_node_name}"
        )

    # Demand constraints
    for demand in demand_nodes:
        demand_node_name = demand['node_name']
        demand_amount = demand['demand_amount']
        model += (
            pl.lpSum(flow[arc['start_node'], demand_node_name] for arc in arcs if arc['end_node'] == demand_node_name) == demand_amount, 
            f"DemandConstraint_{demand_node_name}"
        )

    # Storage constraints
    for storage in storage_nodes:
        inflow = pl.lpSum(flow[arc['start_node'], storage['node_name']] for arc in arcs if arc['end_node'] == storage['node_name'])
        outflow = pl.lpSum(flow[storage['node_name'], arc['end_node']] for arc in arcs if arc['start_node'] == storage['node_name'])
        model += (inflow == outflow, f"StorageConstraint_{storage['node_name']}")

    # Arc capacity constraints
    for arc in arcs:
        if arc['capacity'] is not None:
            start_node = arc['start_node']
            end_node = arc['end_node']
            capacity = arc['capacity']
            model += (
                flow[start_node, end_node] <= capacity, 
                f"CapacityConstraint_{start_node}_{end_node}"
            )

    # Objective function: Minimize total cost
    total_cost = pl.lpSum(
        arc['cost'] * flow[arc['start_node'], arc['end_node']] for arc in arcs
    )
    model += total_cost

    # Solve the model
    model.solve()

    # Print the results
    arc_flows = {}
    if pl.LpStatus[model.status] == 'Optimal':
        
        print("Optimal value:", pl.value(model.objective))

        for arc in arcs:
            start_node = arc['start_node']
            end_node = arc['end_node']

            flow_var = flow[start_node, end_node]
            flow_val = flow_var.varValue

            if flow_val != 0:
                arc_flows[arc['id']] = flow_val
                print(f"Flow from {start_node} to {end_node}: {flow_val}")
    else:
        print("No optimal solution found.")

    return pl.value(model.objective), arc_flows