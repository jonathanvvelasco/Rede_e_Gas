# Module Limits

def expansion_up(make_df,scenario,local):
    # Define the maximum limit of technologies expansion
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    capacity = {"biomass_retrofit_" + local + "_ppl": 20,
        }

    base_capacity = {
        'node_loc': local,
        'year_vtg': [2015, 2020, 2025],
        'unit': 'MW',
    }

    for tec, val in capacity.items():
        df = make_df(base_capacity, technology=tec, value=val)
        scenario.add_par('bound_new_capacity_up', df)

    return scenario
