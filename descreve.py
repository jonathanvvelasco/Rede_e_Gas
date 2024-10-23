# Módulo Descreve (Dados de Historico e de Custo)

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
    # Descreve a vida util de Tecnologias (anos)
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


def expande_tecnologias(make_df,scenario,local,model_horizon):
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


def historico_geracao(make_df,scenario,grid_efficiency,local,history,capacity_factor):
    # Descreve historico de geracao de energia.

    # 1- insere porcentagem de participacao da tecnologia de geracao no ano base
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

    # 2- define valores de energia gerada por cada tecnologia no ano base
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

    # 3- acrescenta valores no parametro "historical_activity"
    for tec, val in old_activity.items():
        df = make_df(
            "historical_activity",
            node_loc=local,
            year_act=history,
            mode="standard",
            time="year",
            unit="GWa",
            technology=tec,
            value=val,
        )
        scenario.add_par("historical_activity", df)

    # 4- define expansao historica como 1/10 da capacidade instalada no ano base
    for tec in old_activity:
        value = old_activity[tec] / (1 * 10 * capacity_factor[tec])
        df = make_df(
            "historical_new_capacity",
            node_loc=local,
            year_vtg=history,
            unit="GWa",
            technology=tec,
            value=value,
        )
        scenario.add_par("historical_new_capacity", df)
    return scenario


def custo_investimento(make_df,scenario,local,model_horizon):
    # Descreve custo de investimento de tecnologias.

    # define custos de investimento
    costs = {
        "oil_ppl": 10000,
        "pch_ppl": 2600,
        "nuclear_g_ppl":3500,
        "biogas_ppl":2400,
        "solar_fotovoltaic_ppl":5900,
        "solar_csp_ppl":4800,
        "onshore_wind_ppl":2500,
        "offshore_wind_ppl":3500,
        "biomass_retrofit_ppl":1500,
        "biomass_greenfield_ppl":1900,
        "GN_open_cycle_ppl":850,
        "GN_combined_cycle_ppl":1200,
        "national_coal_ppl":2100,
        "imported_coal_ppl":2100,
        "large_hydroelectric_ppl":1800,
        "medium_hydroelectric_ppl":2100,
        "bulb": 1,
    }

    # acrescenta valores no parametro "inv_cost"
    for tec, val in costs.items():
        df = make_df(
            "inv_cost",
            node_loc=local,
            year_vtg=model_horizon,
            unit="USD/kW",
            technology=tec,
            value=val,
        )
        scenario.add_par("inv_cost", df)
    return scenario


def custo_fixo(make_df,scenario,local,vintage_years, act_years):
    # Descreve custo fixo de tecnologias.

    # define custos fixos
    costs = {
        "oil_ppl": 20,
        "pch_ppl": 29,
        "nuclear_g_ppl":92,
        "biogas_ppl":169,
        "solar_fotovoltaic_ppl":12,
        "solar_csp_ppl":58,
        "onshore_wind_ppl":31,
        "offshore_wind_ppl":87,
        "biomass_retrofit_ppl":10,
        "biomass_greenfield_ppl":65,
        "GN_open_cycle_ppl":12,
        "GN_combined_cycle_ppl":18,
        "national_coal_ppl":28,
        "imported_coal_ppl":28,
        "large_hydroelectric_ppl":29,
        "medium_hydroelectric_ppl":29,
        "bulb": 1,
    }

    # acrescenta valores no parametro "fix_cost"
    for tec, val in costs.items():
        df = make_df(
            "fix_cost",
            node_loc=local,
            year_vtg=vintage_years,
            year_act=act_years,
            unit="USD/kWa",
            technology=tec,
            value=val,
        )
        scenario.add_par("fix_cost", df)
    return scenario


def custo_variavel(make_df,scenario,local,vintage_years, act_years):
    # Descreve custo variavel de tecnologias.

    # define custos variaveis (custo O&M + custo combustivel)
    costs = {
        "biogas_ppl": 4.0,
        "nuclear_g_ppl":5.7 + 16,
        "national_coal_ppl":4.7 + 36.62,
        "imported_coal_ppl":7.0 + 19.12,
        "GN_open_cycle_ppl":4.0 + 75.60,
        "GN_combined_cycle_ppl":2.3 + 61.60,
        "biomass_retrofit_ppl":14.0,
        "biomass_greenfield_ppl":7.0,
    }

    # acrescenta valores no parametro "var_cost"
    for tec, val in costs.items():
        df = make_df(
            "var_cost",
            node_loc=local,
            year_vtg=vintage_years,
            year_act=act_years,
            mode="standard",
            time="year",
            unit="USD/kWa",
            technology=tec,
            value=val,
        )
        scenario.add_par("var_cost", df)
    return scenario