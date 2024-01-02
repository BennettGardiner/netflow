from django.utils import timezone
import pulp as pl

from netflow_app.models import Solution

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
    for arc in arcs:
        start_node = arc['start_node']
        end_node = arc['end_node']
        flow[start_node, end_node] = pl.LpVariable(f'flow_{start_node}_{end_node}', lowBound=0, cat='Continuous')
        
    # Supply constraints
    for supply in supply_nodes:
        model += (
            pl.lpSum(flow[supply['node_name'], arc['end_node']] for arc in arcs if arc['start_node'] == supply['node_name']) <= supply['supply_amount'], 
            f"SupplyConstraint_{supply['node_name']}"
        )

    # Demand constraints
    for demand in demand_nodes:
        model += (
            pl.lpSum(flow[arc['start_node'], demand['node_name']] for arc in arcs if arc['end_node'] == demand['node_name']) == demand['demand_amount'], 
            f"DemandConstraint_{demand['node_name']}"
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
            flow_val = flow[arc['start_node'], arc['end_node']].varValue
            if flow_val != 0:
                arc_flows[arc['id']] = flow_val
                supply_node = [node['node_name'] for node in supply_nodes if node['node_name'] == arc['start_node']][0]
                demand_node = [node['node_name'] for node in demand_nodes if node['node_name'] == arc['end_node']][0]
                print(f"Flow from {supply_node} to {demand_node}: {flow_val}")
    else:
        print("No optimal solution found.")

    return pl.value(model.objective), arc_flows