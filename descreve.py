# Módulo Link (Input e Output)

def fator_capacidade(make_df,scenario,local,vintage_years, act_years):
    # Descreve Fator de Capacidade de Tecnologias
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    capacity_factor = {
        "oil_ppl": 0.2,
        "pch_ppl": 0.5,
        "nuclear_g_ppl":0.85,
        "biogas_ppl":0.5,
        "solar_fotovoltaic_ppl":0.4,
        "solar_csp_ppl":0.2,
        "onshore_wind_ppl":0.3,
        "offshore_wind_ppl":0.3,
        "biomass_retrofit_ppl":0.67,
        "biomass_greenfield_ppl":0.67,
        "GN_open_cycle_ppl":0.4,
        "GN_combined_cycle_ppl":0.6,
        "national_coal_ppl":0.4,
        "imported_coal_ppl":0.5,
        "large_hydroelectric_ppl":0.5,
        "medium_hydroelectric_ppl":0.55,
        "bulb": 1,
    }

    for tec, val in capacity_factor.items():
        df = make_df(
            "capacity_factor",
            node_loc=local,
            year_vtg=vintage_years,
            year_act=act_years,
            time="year",
            unit="-",
            technology=tec,
            value=val,
        )
        scenario.add_par("capacity_factor", df)

    return scenario, capacity_factor


def vida_util(make_df,scenario,local,model_horizon):
    # Descreve a vida util de Tecnologias
    lifetime = {
    "oil_ppl": 20,
    "pch_ppl": 20,
    "nuclear_g_ppl":20,
    "biogas_ppl":20,
    "solar_fotovoltaic_ppl":20,
    "solar_csp_ppl":20,
    "onshore_wind_ppl":20,
    "offshore_wind_ppl":20,
    "biomass_retrofit_ppl":40,
    "biomass_greenfield_ppl":20,
    "GN_open_cycle_ppl":20,
    "GN_combined_cycle_ppl":20,
    "national_coal_ppl":35,
    "imported_coal_ppl":35,
    "large_hydroelectric_ppl":50,
    "medium_hydroelectric_ppl":50,
    "bulb": 1,
    }

    for tec, val in lifetime.items():
        df = make_df(
            "technical_lifetime",
            node_loc=local,
            year_vtg=model_horizon,
            unit="y",
            technology=tec,
            value=val,
        )
        scenario.add_par("technical_lifetime", df)
    return scenario


def expansao_tecnologias(make_df,scenario,local,model_horizon):
    # Define quais tecnologias sao aptas para expansao.
    growth_technologies = [
        "pch_ppl",
        "nuclear_g_ppl",
        "biogas_ppl",
        "solar_fotovoltaic_ppl",
        "solar_csp_ppl",
        "onshore_wind_ppl",
        "offshore_wind_ppl",
        "biomass_retrofit_ppl",
        "biomass_greenfield_ppl",
        "GN_open_cycle_ppl",
        "GN_combined_cycle_ppl",
        "national_coal_ppl",
        "imported_coal_ppl",
        "large_hydroelectric_ppl",
        "medium_hydroelectric_ppl",
    ]

    for tec in growth_technologies:
        df = make_df(
            "growth_activity_up",
            node_loc=local,
            year_act=model_horizon,
            time="year",
            unit="-",
            technology=tec,
            value=1.0,
        )
        scenario.add_par("growth_activity_up", df)
    return scenario


def historico_geracao(make_df,scenario,grid_efficiency,country,history,capacity_factor):
    # Descreve historico de geracao de energia.
    historic_demand =  60194
    historic_generation = historic_demand / grid_efficiency
    large_hydroelectric_fraction = 0.73532
    pch_fraction = 0.04153
    national_coal_fraction = 0.01339
    gn_fraction = 0.07709
    biomass_fraction = 0.05899
    wind_fraction = 0.03887
    nuclear_fraction  = 0.02834
    oil_fraction = 0.00645



    old_activity = {
        "large_hydroelectric_ppl":(large_hydroelectric_fraction) * historic_generation,
        "oil_ppl": oil_fraction * historic_generation,
        "nuclear_g_ppl": nuclear_fraction*historic_generation,
        "national_coal_ppl": national_coal_fraction* historic_generation,
        "biomass_retrofit_ppl": biomass_fraction * historic_generation,
        "onshore_wind_ppl": wind_fraction* historic_generation,
        "GN_open_cycle_ppl": gn_fraction * historic_generation,
        "pch_ppl": pch_fraction * historic_generation,

    }
    nomes_energias = []
    uso_energias = []


    for i in old_activity.items():
        nomes_energias.append(i[0])
        uso_energias.append(i[1])




    for tec, val in old_activity.items():
        df = make_df(
            "historical_activity",
            node_loc=country,
            year_act=history,
            mode="standard",
            time="year",
            unit="GWa",
            technology=tec,
            value=val,
        )
        scenario.add_par("historical_activity", df)


    for tec in old_activity:
        value = old_activity[tec] / (1 * 10 * capacity_factor[tec])
        df = make_df(
            "historical_new_capacity",
            node_loc=country,
            year_vtg=history,
            unit="GWa",
            technology=tec,
            value=value,
        )
        scenario.add_par("historical_new_capacity", df)
    return scenario