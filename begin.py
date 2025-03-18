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
    scenario.add_set("commodity", ["electricity", "electric_households"])
    scenario.add_set("commodity", ["gas","heating"])
    scenario.add_set("level", ["primary","secondary", "final", "useful"])
    scenario.add_set("technology", technology)
    scenario.add_set("technology", ['transmission_S_SE/CW', 'transmission_SE/CW_S',"transmission_SE/CW_NE", "transmission_NE_SE/CW", "transmission_N_NE", "transmission_NE_N", "transmission_N_SE/CW", "transmission_SE/CW_N"])
    scenario.add_set("mode", "standard")

    return scenario, history, model_horizon, country, nodes


def demand_eletric(pd,scenario,model_horizon,local):
    # Define demand (Mwa)
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    demand_gw_NE = [13.5, 14.4, 15.6]
    demand_gw_N  = [ 8.0,  8.6,  9.3]
    demand_gw_SW = [46.8, 49.9, 54.2]
    demand_gw_S  = [14.2, 15.1, 16.4]

    if local == 'N':
        demand_gw = demand_gw_N
    if local == 'NE':
        demand_gw = demand_gw_NE
    if local == 'SE/CW':
        demand_gw = demand_gw_SW
    if local == 'S':
        demand_gw = demand_gw_S
    demanda = pd.Series(demand_gw, index=pd.Index(model_horizon, name="Time"))
    electric_demand = pd.DataFrame(
        {
            "node": local,
            "commodity": "electric_households",
            "level": "useful",
            "year": model_horizon,
            "time": "year",
            "value": demanda,
            "unit": "GWa",
        }
    )
    scenario.add_par("demand", electric_demand)
    
    return scenario

def demand_gas(pd,scenario,model_horizon,local):
    # Define demand (Mwa)
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    demanda_gas_NE = [ 7.3,	 8.5,	 8.5]
    demanda_gas_N  = [ 0.5,	 0.8,	 0.8]
    demanda_gas_SE = [31.3,	35.8,	40.3]
    demanda_gas_S  = [ 4.0,	 6.0,	 7.5]

    if local == 'N':
        demand_gas = demanda_gas_N
    if local == 'NE':
        demand_gas = demanda_gas_NE
    if local == 'SE/CW':
        demand_gas = demanda_gas_SE
    if local == 'S':
        demand_gas = demanda_gas_S
    demanda = pd.Series(demand_gas, index=pd.Index(model_horizon, name="Time"))
    electric_demand = pd.DataFrame(
        {
            "node": local,
            "commodity": "electric_households",
            "level": "useful",
            "year": model_horizon,
            "time": "year",
            "value": demanda,
            "unit": "GWa",
        }
    )
    scenario.add_par("demand", electric_demand)

    return scenario
