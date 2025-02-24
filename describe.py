# Module Describe (Historical and Costs Data)

def capacity__factor(make_df,scenario,local,vintage_years, act_years):
    # Describe the Technologies Capacity Factor
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    capacity_factor = {
        "oil_" + local + "_ppl": 0.2,
        "pch_" + local + "_ppl": 0.5,
        "nuclear_g_" + local + "_ppl":0.85,
        "biogas_" + local + "_ppl":0.5,
        "solar_photovoltaic_" + local + "_ppl":0.4,
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


def life_time(make_df,scenario,local,model_horizon):
    # Describe the Technologies Lifetimes (years)
    lifetime = {
    "oil_" + local + "_ppl": 20,
    "pch_" + local + "_ppl": 20,
    "nuclear_g_" + local + "_ppl":20,
    "biogas_" + local + "_ppl":20,
    "solar_photovoltaic_" + local + "_ppl":20,
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


def growth__tecnologies(make_df,scenario,local,model_horizon):
    # Define which technologies are able to expansion.

    growth_technologies = [
        "pch_" + local + "_ppl", # "pch_NE_ppl"
        "nuclear_g_" + local + "_ppl",
        "biogas_" + local + "_ppl",
        "solar_photovoltaic_" + local + "_ppl",
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


def historic__generation(make_df,scenario,local,history):
    # Describe the energy generation historic.

    # 1- Insert the participation fraction of each technology in the generation (base year).

    #Historical Demand for electricity (GWa)
    historic_demand_N  = [ 3.848,  5.363,  5.603]
    historic_demand_NE = [ 8.141, 10.261, 10.851]
    historic_demand_SW = [33.421, 38.064, 38.720]
    historic_demand_S  = [ 8.812, 10.937, 11.664]

    #Generation historical activity (GWa)
                    #hydro      #oil   #nuclear #coal  #biomass #wind    #gas    #pch   #PV
    historic_act_N  = [[4,      0.0013, 0,      0,      0,      0,      0,      0.23,   0       ],
                       [5,      0.2925, 0,      0.2785, 0.2042, 0,      1.2667, 0.2667, 0       ], 
                       [7,      0.0013, 0,      0.1294, 0.2022, 0.176,  1.521,  0.4099, 0.0011  ]]
    historic_act_NE = [[4.9,    0.0036, 0,      0,      0.0081, 0.124,  0.8024, 0.31,   0       ],
                       [3,      1.2889, 0,      0.9054, 0.1427, 2.0541, 1.382,  0.16,   0.0016  ],
                       [4,      0.1233, 0,      0.3185, 0.2924, 5.568,  0.7977, 0.2306, 0.4562  ]]
    historic_act_SW = [[29.30,  0.3228, 1.658,  0,      0.3441, 0,      2.0201, 1.64,   0       ],
                       [24.379, 0.4217, 1.6903, 0.0021, 2.2254, 0.0087, 5.193,  1.3644, 0.00004 ],
                       [28.85,  0.0607, 1.5998, 0.0047, 3.2374, 0.0062, 2.317,  1.6146, 0.0008  ]]
    historic_act_S  = [[8.2040, 0,      0,      0,      0.0005, 0.0412, 0.1619, 0.459,  0       ],
                       [10.1951,0.144,  0,      0.8668, 0.1348, 0.4376, 0.3921, 0.5706, 0.00004 ],
                       [4.511,  0.1272, 0,      0.7941, 0.3533, 0.7382, 0.1562, 0.25244,0.2204  ]]

    for j in range(len(history)):


        # 2- Define the generated energy values for each technology in the base year.
        
        if local == 'N':
            old_activity = {
                "large_hydroelectric_" + local + "_ppl": historic_act_N[j][0],
                "oil_" + local + "_ppl": historic_act_N[j][1],
                "nuclear_g_" + local + "_ppl": historic_act_N[j][2],
                "national_coal_" + local + "_ppl": historic_act_N[j][3],
                "biomass_retrofit_" + local + "_ppl": historic_act_N[j][4],
                "onshore_wind_" + local + "_ppl": historic_act_N[j][5],
                "GN_open_cycle_" + local + "_ppl": historic_act_N[j][6],
                "pch_" + local + "_ppl": historic_act_N[j][7],
                "solar_photovoltaic_" + local + "_ppl": historic_act_N[j][8],
                "bulb_" + local: historic_demand_N[j],
            }
        
        if local == 'NE':
            old_activity = {
                "large_hydroelectric_" + local + "_ppl": historic_act_NE[j][0],
                "oil_" + local + "_ppl": historic_act_NE[j][1],
                "nuclear_g_" + local + "_ppl": historic_act_NE[j][2],
                "national_coal_" + local + "_ppl": historic_act_NE[j][3],
                "biomass_retrofit_" + local + "_ppl": historic_act_NE[j][4],
                "onshore_wind_" + local + "_ppl": historic_act_NE[j][5],
                "GN_open_cycle_" + local + "_ppl": historic_act_NE[j][6],
                "pch_" + local + "_ppl": historic_act_NE[j][7],
                "solar_photovoltaic_" + local + "_ppl": historic_act_NE[j][8],
                "bulb_" + local: historic_demand_NE[j],
            }
        
        if local == 'SE/CW':
            old_activity = {
                "large_hydroelectric_" + local + "_ppl": historic_act_SW[j][0],
                "oil_" + local + "_ppl": historic_act_SW[j][1],
                "nuclear_g_" + local + "_ppl": historic_act_SW[j][2],
                "national_coal_" + local + "_ppl": historic_act_SW[j][3],
                "biomass_retrofit_" + local + "_ppl": historic_act_SW[j][4],
                "onshore_wind_" + local + "_ppl": historic_act_SW[j][5],
                "GN_open_cycle_" + local + "_ppl": historic_act_SW[j][6],
                "pch_" + local + "_ppl": historic_act_SW[j][7],
                "solar_photovoltaic_" + local + "_ppl": historic_act_SW[j][8],
                "bulb_" + local: historic_demand_SW[j],
            }
        
        if local == 'S':
            old_activity = {
                "large_hydroelectric_" + local + "_ppl": historic_act_S[j][0],
                "oil_" + local + "_ppl": historic_act_S[j][1],
                "nuclear_g_" + local + "_ppl": historic_act_S[j][2],
                "national_coal_" + local + "_ppl": historic_act_S[j][3],
                "biomass_retrofit_" + local + "_ppl": historic_act_S[j][4],
                "onshore_wind_" + local + "_ppl": historic_act_S[j][5],
                "GN_open_cycle_" + local + "_ppl": historic_act_S[j][6],
                "pch_" + local + "_ppl": historic_act_S[j][7],
                "solar_photovoltaic_" + local + "_ppl": historic_act_S[j][8],
                "bulb_" + local: historic_demand_S[j],
            }

        # 3- Add values to the parameter "historical_activity"
        for tec, val in old_activity.items():
            df = make_df(
                "historical_activity",
                node_loc=local,
                year_act=history[j],
                mode="standard",
                time="year",
                unit="GWa",
                technology=tec,
                value=val,
            )
            scenario.add_par("historical_activity", df)

        # 4- Define the historical expansion as (1/10) of the installed capacity in the base year.
        # for tec in old_activity:
        #     value = old_activity[tec] / (1 * 10 * capacity_factor[tec])
        #     df = make_df(
        #         "historical_new_capacity",
        #         node_loc=local,
        #         year_vtg=history,
        #         unit="GW",
        #         technology=tec,
        #         value=value,
        #     )
        #     scenario.add_par("historical_new_capacity", df)

    return scenario, historic_demand_N, historic_demand_NE, historic_demand_S, historic_demand_SW, historic_act_N, historic_act_NE, historic_act_S, historic_act_SW

def historic__expansion(make_df,scenario,local,history):
    # Describe the historical expansion.

    # Generation historical new capacity (GW)
                         #hydro      #oil   #nuclear #coal  #biomass #wind    #gas    #pch   #PV
    historic_new_cap_N  =  [[8.17,  0.01,   0.00,   0.02,   0.02,   0,      0.12,   0.23,   0       ],
                            [2.00,  0.19,   0.00,   0.26,   0.26,   0,      1.79,   0.0367, 0       ],
                            [9.47,  0.07,   0.00,   0.09,   0.09,   0.43,   0.62,   0.1432, 0.0028  ]]
    historic_new_cap_NE =  [[10.52,  0.73,   0,      0.63,   0.23,   0.26,   1.41,   0.31,   0       ],
                            [0,      0.67,   0,      0.58,   0.21,   3.21,   0.01,   0,      0.004   ],
                            [0,      0.01,   0,      0.01,   0,      10.07,  0,      0,      1.23    ]] 
    historic_new_cap_SW =  [[46.59,  0.29,   1.99,   0,      2.12,   0,      3.47,   1.64,   0       ],
                            [6.36,   0.03,   0.00,   0.0021, 0.25,   0,      0.41,   0,      0.0001  ],
                            [0.88,   0.00,   0.00,   0.0047, 0.00,   0,      0.00,   0,      0.84    ]]
    historic_new_cap_S  =  [[12.81,  0.26,   0.00,   0,      0.46,   0.15,   0.67,   0.46,   0       ],
                            [1.41,   0.00,   0.00,   0.0021, 0.00,   0.82,   0.00,   0.11,   0.0001  ],
                            [0.35,   0.00,   0.00,   0.0047, 0.00,   0.98,   0.00,   0.00,   0.55    ]]
    
    # Adjust values for 5 years average
    historic_new_cap_N  = [[valor / 5 for valor in linha] for linha in historic_new_cap_N]
    historic_new_cap_NE = [[valor / 5 for valor in linha] for linha in historic_new_cap_NE]
    historic_new_cap_SW = [[valor / 5 for valor in linha] for linha in historic_new_cap_SW]
    historic_new_cap_S  = [[valor / 5 for valor in linha] for linha in historic_new_cap_S]

    for j in range(len(history)):


        # 2- Define the generated energy values for each technology in the base year.
        
        if local == 'N':
            old_expansion = {
                "large_hydroelectric_" + local + "_ppl": historic_new_cap_N[j][0],
                "oil_" + local + "_ppl": historic_new_cap_N[j][1],
                "nuclear_g_" + local + "_ppl": historic_new_cap_N[j][2],
                "national_coal_" + local + "_ppl": historic_new_cap_N[j][3],
                "biomass_retrofit_" + local + "_ppl": historic_new_cap_N[j][4],
                "onshore_wind_" + local + "_ppl": historic_new_cap_N[j][5],
                "GN_open_cycle_" + local + "_ppl": historic_new_cap_N[j][6],
                "pch_" + local + "_ppl": historic_new_cap_N[j][7],
                "solar_photovoltaic_" + local + "_ppl": historic_new_cap_N[j][8],
            }
        
        if local == 'NE':
            old_expansion = {
                "large_hydroelectric_" + local + "_ppl": historic_new_cap_NE[j][0],
                "oil_" + local + "_ppl": historic_new_cap_NE[j][1],
                "nuclear_g_" + local + "_ppl": historic_new_cap_NE[j][2],
                "national_coal_" + local + "_ppl": historic_new_cap_NE[j][3],
                "biomass_retrofit_" + local + "_ppl": historic_new_cap_NE[j][4],
                "onshore_wind_" + local + "_ppl": historic_new_cap_NE[j][5],
                "GN_open_cycle_" + local + "_ppl": historic_new_cap_NE[j][6],
                "pch_" + local + "_ppl": historic_new_cap_NE[j][7],
                "solar_photovoltaic_" + local + "_ppl": historic_new_cap_NE[j][8],
            }
        
        if local == 'SE/CW':
            old_expansion = {
                "large_hydroelectric_" + local + "_ppl": historic_new_cap_SW[j][0],
                "oil_" + local + "_ppl": historic_new_cap_SW[j][1],
                "nuclear_g_" + local + "_ppl": historic_new_cap_SW[j][2],
                "national_coal_" + local + "_ppl": historic_new_cap_SW[j][3],
                "biomass_retrofit_" + local + "_ppl": historic_new_cap_SW[j][4],
                "onshore_wind_" + local + "_ppl": historic_new_cap_SW[j][5],
                "GN_open_cycle_" + local + "_ppl": historic_new_cap_SW[j][6],
                "pch_" + local + "_ppl": historic_new_cap_SW[j][7],
                "solar_photovoltaic_" + local + "_ppl": historic_new_cap_SW[j][8],
            }
        
        if local == 'S':
            old_expansion = {
                "large_hydroelectric_" + local + "_ppl": historic_new_cap_S[j][0],
                "oil_" + local + "_ppl": historic_new_cap_S[j][1],
                "nuclear_g_" + local + "_ppl": historic_new_cap_S[j][2],
                "national_coal_" + local + "_ppl": historic_new_cap_S[j][3],
                "biomass_retrofit_" + local + "_ppl": historic_new_cap_S[j][4],
                "onshore_wind_" + local + "_ppl": historic_new_cap_S[j][5],
                "GN_open_cycle_" + local + "_ppl": historic_new_cap_S[j][6],
                "pch_" + local + "_ppl": historic_new_cap_S[j][7],
                "solar_photovoltaic_" + local + "_ppl": historic_new_cap_S[j][8],
            }

        # 3- Add values to the parameter "historical_new_capacity"
        for tec, val in old_expansion.items():
                df = make_df(
                "historical_new_capacity",
                node_loc=local,
                year_vtg=history[j],
                unit="GW",
                technology=tec,
                value=val,
                )
                scenario.add_par("historical_new_capacity", df)

    return scenario

def inv_costs(make_df,scenario,local,model_horizon):
    # Describe the investment costs of the technologies.

    # Define the investment costs
    costs = {
        "oil_" + local + "_ppl": 10000,
        "pch_" + local + "_ppl": 2600,
        "nuclear_g_" + local + "_ppl":3500,
        "biogas_" + local + "_ppl":2400,
        "solar_photovoltaic_" + local + "_ppl":1100,
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
            unit="mi USD/GW",
            technology=tec,
            value=val,
        )
        scenario.add_par("inv_cost", df)
    return scenario


def fix_costs(make_df,scenario,local,vintage_years, act_years):
    # Describe the fix costs of technologies.

    # Define fix costs
    costs = {
        "oil_" + local + "_ppl": 20,
        "pch_" + local + "_ppl": 29,
        "nuclear_g_" + local + "_ppl":92,
        "biogas_" + local + "_ppl":169,
        "solar_photovoltaic_" + local + "_ppl":12,
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
            unit="mi USD/GW-a",
            technology=tec,
            value=val,
        )
        scenario.add_par("fix_cost", df)
    return scenario


def var_costs(make_df,scenario,local,vintage_years, act_years):
    # Describe the variable costs of the technologies.

    # Define variable costs (O&M cost + fuel cost) inserted in USD/MWh
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
    convertion_factor = 8760/1000 #convert USD/MWh to mi_USD/GWa
    for tec, val in costs.items():
        df = make_df(
            "var_cost",
            node_loc=local,
            year_vtg=vintage_years,
            year_act=act_years,
            mode="standard",
            time="year",
            unit="mi USD/GWa",
            technology=tec,
            value=val*convertion_factor,
        )
        scenario.add_par("var_cost", df)
    return scenario
