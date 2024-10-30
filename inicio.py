# Modulo Definicoes

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
    nodes = ['N','NE','SE/CE', 'S']
    space_level = 'subsystem'
    scenario.add_set('lvl_spatial', space_level)
    for node in nodes:
        scenario.add_set('node', node)
        scenario.add_set('map_spatial_hierarchy', [space_level, node, country])
    scenario.set('map_spatial_hierarchy')

    # Define taxa de desconto anual
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    scenario.add_par("interestrate", model_horizon, value=0.08, unit="-")

    # Define tecnologias 
    # ^^^^^^^^^^^^^^^^^^
    scenario.add_set("commodity", ["electricity", "electric_households"])
    scenario.add_set("commodity", ["gas","gas households"])
    scenario.add_set("level", ["primary","secondary", "final", "useful"])
    scenario.add_set("technology", ["oil_ppl", "pch_ppl","nuclear_g_ppl", "biogas_ppl", "solar_fotovoltaic_ppl", "solar_csp_ppl","onshore_wind_ppl", "offshore_wind_ppl","biomass_retrofit_ppl", "biomass_greenfield_ppl","GN_open_cycle_ppl", "GN_combined_cycle_ppl","national_coal_ppl", "imported_coal_ppl","large_hydroelectric_ppl", "medium_hydroelectric_ppl","grid", "bulb"])
    scenario.add_set("technology", ['transmissao_S_SE', 'transmissao_SE_S'])
    scenario.add_set("technology", ["electric_housing"])
    scenario.add_set("mode", "standard")

    return scenario, history, model_horizon, country, nodes


def demanda(pd,scenario,model_horizon,local):
    # Define demanda em MWmédios (ao ano)
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    demand_gw = [77.883, 100.861, 119.496]
    demand_mw = [valor * 1000 for valor in demand_gw]
    demanda = pd.Series(demand_mw, index=pd.Index(model_horizon, name="Time"))
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