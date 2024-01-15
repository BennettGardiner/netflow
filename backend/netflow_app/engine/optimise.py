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
    for timestep in range(timesteps):
        
        for arc in arcs:
            # Decision variables for flow on each arc at each timestep
            start_node = arc['start_node']
            end_node = arc['end_node']
            flow[start_node, end_node, timestep] = pl.LpVariable(f'flow_{start_node}_{end_node}_{timestep}', lowBound=0, cat='Continuous')
            print(f"Created flow variable for {start_node} to {end_node} at timestep {timestep}")

            # Binary variables to indicate whether an arc is used at each timestep
            arc_usage[start_node, end_node, timestep] = pl.LpVariable(f'arc_usage_{start_node}_{end_node}_{timestep}', cat='Binary')

        # Create storage arcs with the same start and end node
        for storage in storage_nodes:
            storage_node_name = storage.node_name
            flow[storage_node_name, storage_node_name, timestep] = pl.LpVariable(f'flow_{storage_node_name}_{storage_node_name}_{timestep}', lowBound=0, cat='Continuous')

    # Supply constraints over all timesteps
    for supply in supply_nodes:
        supply_node_name = supply['node_name']
        supply_amount = supply['supply_amount']
        total_supply_flow = pl.lpSum(flow[supply_node_name, arc['end_node'], timestep] 
                                    for arc in arcs 
                                    for timestep in range(timesteps) 
                                    if arc['start_node'] == supply_node_name)
        model += (
            total_supply_flow <= supply_amount, 
            f"SupplyConstraint_{supply_node_name}"
        )
        print(f"Created supply constraint for {supply_node_name} of {supply_amount} over all timesteps")

    # Demand constraints over all timesteps
    for demand in demand_nodes:
        demand_node_name = demand['node_name']
        demand_amount = demand['demand_amount']
        total_demand_fulfilled = pl.lpSum(flow[arc['start_node'], demand_node_name, timestep] 
                                        for arc in arcs 
                                        for timestep in range(timesteps) 
                                        if arc['end_node'] == demand_node_name)
        model += (
            total_demand_fulfilled == demand_amount, 
            f"DemandConstraint_{demand_node_name}"
        )
        print(f"Created demand constraint for {demand_node_name} of {demand_amount} over all timesteps")

    # Storage balance constraints over all timesteps
    for storage in storage_nodes:
        storage_node_name = storage.node_name
        initial_amount = storage['initial_amount']

        for timestep in range(timesteps):
            inflow = pl.lpSum(flow[arc['start_node'], storage_node_name, timestep] for arc in arcs if arc['end_node'] == storage_node_name)
            outflow = pl.lpSum(flow[storage_node_name, arc['end_node'], timestep] for arc in arcs if arc['start_node'] == storage_node_name)

            previous_storage_level = initial_amount if timestep == 0 else flow[storage_node_name, storage_node_name, timestep-1]
            current_storage_level = flow[storage_node_name, storage_node_name, timestep]
            
            model += (inflow + previous_storage_level == current_storage_level + outflow, f"StorageConstraint_{storage_node_name}_{timestep}")
            print(f"""Created storage balance constraint for {storage_node_name} at timestep {timestep} of 
                  {inflow} + {previous_storage_level} = {current_storage_level} + {outflow}""")
    
    # Arc capacity constraints
    for timestep in range(timesteps):
        for arc in arcs:
            if arc['capacity'] is not None:
                start_node = arc['start_node']
                end_node = arc['end_node']
                capacity = arc['capacity']
                model += (
                    flow[start_node, end_node, timestep] <= capacity, 
                    f"CapacityConstraint_{start_node}_{end_node}_{timestep}"
                )
                print(f"Created capacity constraint for {start_node} to {end_node} of capacity {capacity} at timestep {timestep}")


    # Objective function: Minimize total cost
    total_cost = pl.lpSum(
        arc['cost'] * flow[arc['start_node'], arc['end_node'], timestep] for arc in arcs for timestep in range(timesteps)
    )
    model += total_cost

    # Construct the objective function string
    objective_function_str = " + ".join([
        f"{arc['cost']}*flow_{arc['start_node']}_{arc['end_node']}_t{timestep}"
        for arc in arcs 
        for timestep in range(timesteps)
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
                flow_val = flow[arc['start_node'], arc['end_node'], timestep].varValue
                if flow_val != 0:
                    timestep_arc_flows[timestep][arc['id']] = {
                        "amount": flow_val,
                        "cost": arc['cost'],    
                        "start_node": arc['start_node'],
                        "end_node": arc['end_node'],
                    }
    else:
        print("No optimal solution found.")
    
    return pl.value(model.objective), timestep_arc_flows

