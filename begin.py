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
    scenario.add_set("commodity", ["gas_onland", "gas_undersea", "gnl_imported", "natural_gas", "gas_extracted"])
    scenario.add_set("technology", ["GNL", "pipelines", "boiler", "GASBOL", "UPGN", "Gas_Offshore", "Gas_Onshore", "Gas_Reinjection", "gas_transport_S_SE/CW", "gas_transport_SE/CW_S"])

    # Add Fossil Resources
    scenario.add_set("level_resource", "resource")
    scenario.add_set("grade", ["onshore_gas", "offshore_gas"])

    return scenario, history, model_horizon, country, nodes, technology


def resource_gas_onshore(pd,scenario,local):
    # Define resources of gas onshore (MMm3/day)
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    gas_resource_N = 127.5
    gas_resource_NE = 153.7
    gas_resource_SE = 2.7
    gas_resource_S = 2.8     #Valor ficticio, falta o BRABOL. Valor real é 2.8 MMm3/dia

    # Check local node
    if local == 'N':
        potential_gas = gas_resource_N
    if local == 'NE':
        potential_gas = gas_resource_NE
    if local == 'SE/CW':
        potential_gas = gas_resource_SE
    if local == 'S':
        potential_gas = gas_resource_S

    # Convert data to dataframe format
    resource_gas = pd.DataFrame(
        {
            "node": local,
            "commodity": "gas_onland",
            "grade": "onshore_gas",
            "value": [potential_gas],
            "unit": "MMm3/day",
        }
    )
    scenario.add_par("resource_volume", resource_gas)

    return scenario

def resource_gas_offshore(pd,scenario,local):
    # Define resources of gas offshore (MMm3/day)
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    gas_resource_NE = 7.9
    gas_resource_SE = 1201.3

    # Check local node
    if local == 'NE':
        potential_gas = gas_resource_NE
    if local == 'SE/CW':
        potential_gas = gas_resource_SE
    if local == 'N' or local == 'S':
        potential_gas = 0

    # Convert data to dataframe format
    resource_gas = pd.DataFrame(
        {
            "node": local,
            "commodity": "gas_undersea",
            "grade": "offshore_gas",
            "value": [potential_gas],
            "unit": "MMm3/day",
        }
    )
    scenario.add_par("resource_volume", resource_gas)

    return scenario
