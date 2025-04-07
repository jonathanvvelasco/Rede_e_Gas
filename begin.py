# Module Begin

def definitions(pd,scenario):
    # Define historical year and simulation years
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    history = [2010, 2015, 2020]
    model_horizon = [2025, 2030, 2035]
    scenario.add_horizon(year=history + model_horizon, firstmodelyear=model_horizon[0])

    # Define country and subdivisions
    country = "Brazil"
    scenario.add_spatial_sets({"country": country})

    #Defining regions
    scenario.set('map_spatial_hierarchy')
    nodes = ['N','NE','SE/CW', 'S']
    space_level = 'subsystem'
    scenario.add_set('lvl_spatial', space_level)
    for node in nodes:
        scenario.add_set('node', node)
        scenario.add_set('map_spatial_hierarchy', [space_level, node, country])
    scenario.set('map_spatial_hierarchy')

    # Define Annual Interest Rate 
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    scenario.add_par("interestrate", model_horizon, value=0.08, unit="-")

    # Define technologies
    # ^^^^^^^^^^^^^^^^^^
    tecs = ["oil_ppl", "pch_ppl","nuclear_g_ppl", "biogas_ppl", "solar_photovoltaic_ppl", "solar_csp_ppl","onshore_wind_ppl", "offshore_wind_ppl","biomass_retrofit_ppl", "biomass_greenfield_ppl","GN_open_cycle_ppl", "GN_combined_cycle_ppl","national_coal_ppl", "imported_coal_ppl","large_hydroelectric_ppl", "medium_hydroelectric_ppl","grid", "bulb"]
    technology = []

    # Define technologies for each region
    for k in nodes:
        for j in range(len(tecs)):
            tec = ""
            if "ppl" in tecs[j]:
                for n in tecs[j].split("_"):
                    if n != "ppl":
                        tec = tec + n + "_"
                    else:
                        tec = tec + k + "_ppl"

                technology.append(tec)

            else:
                technology.append(tecs[j] + "_" + k)

    # Define sets
    scenario.add_set("level", ["resource", "primary", "secondary", "final", "useful"])
    scenario.add_set("mode", "standard")

    # Sets on the Electricity Sector
    scenario.add_set("commodity", ["electricity", "electric_households"])
    scenario.add_set("technology", technology)
    scenario.add_set("technology", ['transmission_S_SE/CW', 'transmission_SE/CW_S',"transmission_SE/CW_NE", "transmission_NE_SE/CW", "transmission_N_NE", "transmission_NE_N", "transmission_N_SE/CW", "transmission_SE/CW_N"])
    
    # Sets on the Natural Gas Sector
    scenario.add_set("commodity", ["gas_underground", "gnl_imported", "natural_gas", "gas_extracted"])
    scenario.add_set("technology", ["GNL", "pipelines", "boiler", "GASBOL", "UPGN", "Gas_Offshore", "Gas_Onshore", "Gas_Reinjection"])

    # Add Fossil Resources
    scenario.add_set("level_resource", "resource")
    scenario.add_set("grade", ["natural_gas"])

    return scenario, history, model_horizon, country, nodes


def demand_eletric(pd,scenario,model_horizon,local):
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

def demand_gas(pd,scenario,model_horizon,local):
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


def potential_gas(pd,scenario,local):
    # Define demand (MMm3/day)
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    resource_gas_NE = 40
    resource_gas_N  = 50
    resource_gas_SE = 70
    resource_gas_S  = 80

    # Check local node
    if local == 'N':
        potential_gas = resource_gas_N
    if local == 'NE':
        potential_gas = resource_gas_NE
    if local == 'SE/CW':
        potential_gas = resource_gas_SE
    if local == 'S':
        potential_gas = resource_gas_S

    # Convert data to dataframe format
    gas_resource = pd.DataFrame(
        {
            "node": local,
            "commodity": "gas_underground",
            "grade": "natural_gas",
            "value": [potential_gas],
            "unit": "MMm3/day",
        }
    )
    scenario.add_par("resource_volume", gas_resource)

    return scenario