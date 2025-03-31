# Module Limits

def expansion_up(make_df,scenario,local):
    # Define the maximum limit of technologies expansion
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    capacity = {
            "biomass_retrofit_" + local + "_ppl": 0.5,
            # "solar_photovoltaic_" + local + "_ppl": 2,
        }

    base_capacity = {
        'node_loc': local,
        'year_vtg': [2025, 2030, 2035],
        'unit': 'GW',
    }

    for tec, val in capacity.items():
        df = make_df(base_capacity, technology=tec, value=val)
        scenario.add_par('bound_new_capacity_up', df)

    return scenario

def activity_up(make_df,scenario,local):
    # Define the maximum limit of technologies activity
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    activity = {
            "Gas_Reinjection": 2.0,
        }

    base_activity = {
        'node_loc': local,
        'year_act': [2025, 2030, 2035],
        'mode': 'standard',
        'time': 'year',
        'unit': 'GWa',
    }

    if local == "NE":
        for tec, val in activity.items():
            df = make_df(base_activity, technology=tec, value=val)
            scenario.add_par('bound_activity_lo', df)

    return scenario