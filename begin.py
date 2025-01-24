# Module Begin

def definitions(pd,scenario):
    # Define historical year and simulation years
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    history = [2010]
    model_horizon = [2015, 2020, 2025]
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
    tecs = ["oil_ppl", "pch_ppl","nuclear_g_ppl", "biogas_ppl", "solar_fotovoltaic_ppl", "solar_csp_ppl","onshore_wind_ppl", "offshore_wind_ppl","biomass_retrofit_ppl", "biomass_greenfield_ppl","GN_open_cycle_ppl", "GN_combined_cycle_ppl","national_coal_ppl", "imported_coal_ppl","large_hydroelectric_ppl", "medium_hydroelectric_ppl","grid", "bulb"]
    technology = []

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
            
            
    
    
                    
                
            
    scenario.add_set("commodity", ["electricity", "electric_households"])
    scenario.add_set("commodity", ["gas","gas households"])
    scenario.add_set("level", ["primary","secondary", "final", "useful"])
    scenario.add_set("technology", technology)
    scenario.add_set("technology", ['transmission_S_SE/CW', 'transmission_SE/CW_S',"transmission_SE/CW_NE", "transmission_NE_SE/CW", "transmission_N_NE", "transmission_NE_N", "transmission_N_SE/CW", "transmission_SE/CW_N"])
    scenario.add_set("mode", "standard")

    return scenario, history, model_horizon, country, nodes


def demand(pd,scenario,model_horizon,local):
    # Define demand (Mwa)
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    demand_gw = [77.883, 100.861, 119.496]
    demand_gw_N  = [ 4.63,  5.52,  7.10]
    demand_gw_NE = [ 9.20, 10.74, 12.33]
    demand_gw_SW = [35.84, 38.62, 42.91]
    demand_gw_s  = [10.21, 11.42, 12.95]
    if local == 'N':
        demand_gw = demand_gw
    
    # demand_mw = [valor * 1000 for valor in demand_gw]
    demanda = pd.Series(demand_gw, index=pd.Index(model_horizon, name="Time"))
    electric_demand = pd.DataFrame(
        {
            "node": local,
            "commodity": "electric_households",
            "level": "useful",
            "year": model_horizon,
            "time": "year",
            "value": (demanda).round(),
            "unit": "MWa",
        }
    )
    scenario.add_par("demand", electric_demand)

    return scenario
