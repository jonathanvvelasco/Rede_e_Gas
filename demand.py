# Module Demand

def electricity(pd,scenario,model_horizon,local):
    # Define demand (GWa)
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    demand_gw_NE = [13.5, 14.4, 15.6]
    demand_gw_N  = [ 8.0,  8.6,  9.3]
    demand_gw_SW = [46.8, 49.9, 54.2]
    demand_gw_S  = [14.2, 15.1, 16.4]

    # Check local node
    if local == 'N':
        demand_gw = demand_gw_N
    if local == 'NE':
        demand_gw = demand_gw_NE
    if local == 'SE/CW':
        demand_gw = demand_gw_SW
    if local == 'S':
        demand_gw = demand_gw_S

    # Convert data to dataframe format
    demand = pd.Series(demand_gw, index=pd.Index(model_horizon, name="Time"))
    electric_demand = pd.DataFrame(
        {
            "node": local,
            "commodity": "electric_households",
            "level": "useful",
            "year": model_horizon,
            "time": "year",
            "value": demand,
            "unit": "GWa",
        }
    )
    scenario.add_par("demand", electric_demand)
    
    return scenario

def natural_gas(pd,scenario,model_horizon,local):
    # Define demand (MMm3/day)
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    demand_gas_NE = [ 7.3,	 8.5,	 8.5]
    demand_gas_N  = [ 0.5,	 0.8,	 0.8]
    demand_gas_SE = [31.3,	35.8,	40.3]
    demand_gas_S  = [ 4.0,	 6.0,	 7.5]

    # Check local node
    if local == 'N':
        demand_gas = demand_gas_N
    if local == 'NE':
        demand_gas = demand_gas_NE
    if local == 'SE/CW':
        demand_gas = demand_gas_SE
    if local == 'S':
        demand_gas = demand_gas_S

    # Convert data to dataframe format
    demand = pd.Series(demand_gas, index=pd.Index(model_horizon, name="Time"))
    gas_demand = pd.DataFrame(
        {
            "node": local,
            "commodity": "natural_gas",
            "level": "useful",
            "year": model_horizon,
            "time": "year",
            "value": demand,
            "unit": "MMm3/day",
        }
    )
    scenario.add_par("demand", gas_demand)

    return scenario