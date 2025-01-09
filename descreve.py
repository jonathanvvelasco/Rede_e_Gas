
# Module Descreve (Historical and Costs Data)

def fator_capacidade(make_df,scenario,local,vintage_years, act_years):
    # Describe the Technologies Capacity Factor
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    capacity_factor = {
        "oil_" + local + "_ppl": 0.2,
        "pch_" + local + "_ppl": 0.5,
        "nuclear_g_" + local + "_ppl":0.85,
        "biogas_" + local + "_ppl":0.5,
        "solar_fotovoltaic_" + local + "_ppl":0.4,
        "solar_csp_" + local + "_ppl":0.2,
        "onshore_wind_" + local + "_ppl":0.3,
        "offshore_wind_" + local + "_ppl":0.3,
        "biomass_retrofit_" + local + "_ppl":0.67,
        "biomass_greenfield_" + local + "_ppl":0.67,
        "GN_open_cycle_" + local + "_ppl":0.4,
        "GN_combined_cycle_" + local + "_ppl":0.6,
        "national_coal_" + local + "_ppl":0.4,
        "imported_coal_" + local + "_ppl":0.5,
        "large_hydroelectric_" + local + "_ppl":0.5,
        "medium_hydroelectric_" + local + "_ppl":0.55,
        "bulb_" + local: 1,
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
    # Describe the Technologies Lifetimes (years)
    lifetime = {
    "oil_" + local + "_ppl": 20,
    "pch_" + local + "_ppl": 20,
    "nuclear_g_" + local + "_ppl":20,
    "biogas_" + local + "_ppl":20,
    "solar_fotovoltaic_" + local + "_ppl":20,
    "solar_csp_" + local + "_ppl":20,
    "onshore_wind_" + local + "_ppl":20,
    "offshore_wind_" + local + "_ppl":20,
    "biomass_retrofit_" + local + "_ppl":40,
    "biomass_greenfield_" + local + "_ppl":20,
    "GN_open_cycle_" + local + "_ppl":20,
    "GN_combined_cycle_" + local + "_ppl":20,
    "national_coal_" + local + "_ppl":35,
    "imported_coal_" + local + "_ppl":35,
    "large_hydroelectric_" + local + "_ppl":50,
    "medium_hydroelectric_" + local + "_ppl":50,
    "bulb_" + local: 1,
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
    # Define which technologies are able to expansion.

    growth_technologies = [
        "pch_" + local + "_ppl", # "pch_NE_ppl"
        "nuclear_g_" + local + "_ppl",
        "biogas_" + local + "_ppl",
        "solar_fotovoltaic_" + local + "_ppl",
        "solar_csp_" + local + "_ppl",
        "onshore_wind_" + local + "_ppl",
        "offshore_wind_" + local + "_ppl",
        "biomass_retrofit_" + local + "_ppl",
        "biomass_greenfield_" + local + "_ppl",
        "GN_open_cycle_" + local + "_ppl",
        "GN_combined_cycle_" + local + "_ppl",
        "national_coal_" + local + "_ppl",
        "imported_coal_" + local + "_ppl",
        "large_hydroelectric_" + local + "_ppl",
        "medium_hydroelectric_" + local + "_ppl",
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
    # Describe the energy generation historic.

    # 1- Insert the participation fraction of each technology in the generation (base year).
    historic_demand =  60.194 # -> Demand (GWa)
    historic_generation = historic_demand / grid_efficiency
    large_hydroelectric_fraction = 0.73532
    pch_fraction = 0.04153
    national_coal_fraction = 0.01339
    gn_fraction = 0.07709
    biomass_fraction = 0.05899
    wind_fraction = 0.03887
    nuclear_fraction  = 0.02834
    oil_fraction = 0.00645

    # 2- Define the generated energy values for each technology in the base year.
    old_activity = {
        "large_hydroelectric_" + local + "_ppl":(large_hydroelectric_fraction) * historic_generation,
        "oil_" + local + "_ppl": oil_fraction * historic_generation,
        "nuclear_g_" + local + "_ppl": nuclear_fraction*historic_generation,
        "national_coal_" + local + "_ppl": national_coal_fraction* historic_generation,
        "biomass_retrofit_" + local + "_ppl": biomass_fraction * historic_generation,
        "onshore_wind_" + local + "_ppl": wind_fraction* historic_generation,
        "GN_open_cycle_" + local + "_ppl": gn_fraction * historic_generation,
        "pch_" + local + "_ppl": pch_fraction * historic_generation,
    }

    if (local == 'S') or (local == 'N'):
        old_activity["nuclear_g_"+local+"_ppl"]=0

    # 3- Add values to the parameter "historical_activity"
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

    # 4- Define the historical expansion as (1/10) of the installed capacity in the base year.
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
    # Describe the investment costs of the technologies.

    # Define the investment costs
    costs = {
        "oil_" + local + "_ppl": 10000,
        "pch_" + local + "_ppl": 2600,
        "nuclear_g_" + local + "_ppl":3500,
        "biogas_" + local + "_ppl":2400,
        "solar_fotovoltaic_" + local + "_ppl":5900,
        "solar_csp_" + local + "_ppl":4800,
        "onshore_wind_" + local + "_ppl":2500,
        "offshore_wind_" + local + "_ppl":3500,
        "biomass_retrofit_" + local + "_ppl":1500,
        "biomass_greenfield_" + local + "_ppl":1900,
        "GN_open_cycle_" + local + "_ppl":850,
        "GN_combined_cycle_" + local + "_ppl":1200,
        "national_coal_" + local + "_ppl":2100,
        "imported_coal_" + local + "_ppl":2100,
        "large_hydroelectric_" + local + "_ppl":1800,
        "medium_hydroelectric_" + local + "_ppl":2100,
        "bulb_" + local: 1,
    }

    # Add values to the parameter "inv_cost"
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
    # Describe the fix costs of technologies.

    # Define fix costs
    costs = {
        "oil_" + local + "_ppl": 20,
        "pch_" + local + "_ppl": 29,
        "nuclear_g_" + local + "_ppl":92,
        "biogas_" + local + "_ppl":169,
        "solar_fotovoltaic_" + local + "_ppl":12,
        "solar_csp_" + local + "_ppl":58,
        "onshore_wind_" + local + "_ppl":31,
        "offshore_wind_" + local + "_ppl":87,
        "biomass_retrofit_" + local + "_ppl":10,
        "biomass_greenfield_" + local + "_ppl":65,
        "GN_open_cycle_" + local + "_ppl":12,
        "GN_combined_cycle_" + local + "_ppl":18,
        "national_coal_" + local + "_ppl":28,
        "imported_coal_" + local + "_ppl":28,
        "large_hydroelectric_" + local + "_ppl":29,
        "medium_hydroelectric_" + local + "_ppl":29,
        "bulb_" + local: 1,
    }

    # Add values to the parameter "fix_cost"
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
    # Describe the variable costs of the technologies.

    # Define variable costs (O&M cost + fuel cost)
    costs = {
        "biogas_" + local + "_ppl": 4.0,
        "nuclear_g_" + local + "_ppl":5.7 + 16,
        "national_coal_" + local + "_ppl":4.7 + 36.62,
        "imported_coal_" + local + "_ppl":7.0 + 19.12,
        "GN_open_cycle_" + local + "_ppl":4.0 + 75.60,
        "GN_combined_cycle_" + local + "_ppl":2.3 + 61.60,
        "biomass_retrofit_" + local + "_ppl":14.0,
        "biomass_greenfield_" + local + "_ppl":7.0,
    }


    # Add values to the parameter "var_cost"
    for tec, val in costs.items():
        df = make_df(
            "var_cost",
            node_loc=local,
            year_vtg=vintage_years,
            year_act=act_years,
            mode="standard",
            time="year",
            unit="USD/MWh",
            technology=tec,
            value=val,
        )
        scenario.add_par("var_cost", df)
    return scenario
