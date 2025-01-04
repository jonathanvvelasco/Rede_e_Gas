# Modulo Limites

def expansao_up(make_df,scenario,local):
    # Define limite maximo de expansao de tecnologias
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    capacity = {"biomass_retrofit_ppl": 20,
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