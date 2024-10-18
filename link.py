# Módulo Link (Input e Output)

def definicoes(pd,scenario):
    # Define ano historico e anos de simulacao
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    history = [2010]
    model_horizon = [2015, 2020, 2025]
    scenario.add_horizon(year=history + model_horizon, firstmodelyear=model_horizon[0])

    # Define pais e subdivisoes
    country = "Brazil"
    scenario.add_spatial_sets({"country": country})

    #Definindo regiões
    scenario.set('map_spatial_hierarchy')
    nodes = ['SE/CE']
    space_level = 'province'
    scenario.add_set('lvl_spatial', space_level)
    for node in nodes:
        scenario.add_set('node', node)
        scenario.add_set('map_spatial_hierarchy', [space_level, node, country])
    scenario.set('map_spatial_hierarchy')

    # Define tecnologias 
    # ^^^^^^^^^^^^^^^^^^
    scenario.add_set("commodity", ["electricity", "light"])
    scenario.add_set("level", ["secondary", "final", "useful"])
    scenario.add_set("technology", ["oil_ppl", "pch_ppl","nuclear_g_ppl", "biogas_ppl", "solar_fotovoltaic_ppl", "solar_csp_ppl","onshore_wind_ppl", "offshore_wind_ppl","biomass_retrofit_ppl", "biomass_greenfield_ppl","GN_open_cycle_ppl", "GN_combined_cycle_ppl","national_coal_ppl", "imported_coal_ppl","large_hydroelectric_ppl", "medium_hydroelectric_ppl","grid", "bulb"])
    scenario.add_set("mode", "standard")

    # Define demanda em MWmédios
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^
    demanda = pd.Series([77883, 100861, 119496], index=pd.Index(model_horizon, name="Time"))
    light_demand = pd.DataFrame(
        {
            "node": country,
            "commodity": "light",
            "level": "useful",
            "year": model_horizon,
            "time": "year",
            "value": (demanda).round(),
            "unit": "MWa",
        }
    )
    scenario.add_par("demand", light_demand)

    return scenario