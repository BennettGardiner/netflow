from django.utils import timezone
import pulp as pl

from netflow_app.models import Solution

def optimise_network(data):
    print("Optimising network using data")
    
    parameters = data['parameters']
    timesteps = parameters['timesteps']
    supply_nodes = data['supply_nodes']
    demand_nodes = data['demand_nodes']
    storage_nodes = data['storage_nodes']
    arcs = data['arcs']

    # Initialize the model
    model = pl.LpProblem("NetworkOptimization", pl.LpMinimize)

    flow = {}
    arc_usage = {}
    for arc in arcs:
        # Decision variables for flow on each engine arc
        start_node = arc.start_engine_node.id
        end_node = arc.end_engine_node.id
        flow[start_node, end_node] = pl.LpVariable(f'flow_{start_node}_{end_node}', lowBound=0, cat='Continuous')
        print(f"Created flow variable for {start_node} to {end_node}")

        # Binary variables to indicate whether an engine arc is used
        arc_usage[start_node, end_node] = pl.LpVariable(f'arc_usage_{start_node}_{end_node}', cat='Binary')
    
    # Supply constraints
    for supply in supply_nodes:
        if supply.timestep == 0:
            supply_node_name = supply.id
            supply_amount = supply.supply_amount
            total_supply_flow = pl.lpSum(flow[supply_node_name, arc.end_engine_node.id] 
                                        for arc in arcs 
                                        if arc.start_engine_node.id == supply_node_name)
            model += (
                total_supply_flow <= supply_amount, 
                f"SupplyConstraint_{supply_node_name}"
            )
            print(f"Created supply constraint for {supply_node_name} of {supply_amount}")

    # Demand constraints
    for demand in demand_nodes:
        if demand.timestep == timesteps - 1:
            demand_node_name = demand.id
            demand_amount = demand.demand_amount
            total_demand_fulfilled = pl.lpSum(flow[arc.start_engine_node.id, demand_node_name] 
                            for arc in arcs 
                            if arc.end_engine_node.id == demand_node_name)
            model += (
                total_demand_fulfilled == demand_amount, 
                f"DemandConstraint_{demand_node_name}"
            )
            print(f"Created demand constraint for {demand_node_name} of {demand_amount}")
    
    # Arc capacity constraints
    for arc in arcs:
        if arc.capacity is not None:
            start_node = arc.start_engine_node.id
            end_node = arc.end_engine_node.id
            capacity = arc.capacity
            model += (
                flow[start_node, end_node] <= capacity, 
                f"CapacityConstraint_{start_node}_{end_node}"
            )
            print(f"Created capacity constraint for {start_node} to {end_node} of capacity {capacity}")


    # Objective function: Minimize total cost
    total_cost = pl.lpSum(
        arc.cost * flow[arc.start_engine_node.id, arc.end_engine_node.id] for arc in arcs
    )
    model += total_cost

    # Construct the objective function string
    objective_function_str = " + ".join([
        f"{arc.cost}*flow_{arc.start_engine_node.id}_{arc.end_engine_node.id}"
        for arc in arcs
    ])

    print("Created objective function:", objective_function_str)

    # Solve the model
    model.solve()

    # Print the results
    timestep_arc_flows = {}
    if pl.LpStatus[model.status] == 'Optimal':
        print("Optimal value:", pl.value(model.objective))

        for timestep in range(timesteps):
            timestep_arc_flows[timestep] = {}
            
        for arc in arcs:
            flow_val = flow[arc.start_engine_node.id, arc.end_engine_node.id].varValue
            if flow_val != 0:
                start_timestep = arc.start_engine_node.timestep
                end_timestep = arc.end_engine_node.timestep
                for timestep in range(start_timestep, end_timestep):
                    timestep_arc_flows[timestep][arc.id] = {
                        "amount": flow_val,
                        "cost": arc.cost if timestep == start_timestep else 0,
                        "start_node": arc.start_engine_node.id,
                        "end_node": arc.end_engine_node.id,
                    }
        
    else:
        print("No optimal solution found.")

    
    return pl.value(model.objective), timestep_arc_flows

