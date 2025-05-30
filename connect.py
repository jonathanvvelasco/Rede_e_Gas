# Module Connect (Input and Output)

def base(make_df,scenario,local):
    # Define the basis link between input and output
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # 1- Read the construction years and production years
    year_df = scenario.vintage_and_active_years()
    vintage_years, act_years = year_df["year_vtg"], year_df["year_act"]
    # 2- Create a basis class for input and output
    base = dict(
        node_loc=local,
        year_vtg=vintage_years,
        year_act=act_years,
        mode="standard",
        time="year",
        unit="-",
    )
    base_input = make_df("input", **base, node_origin=local, time_origin="year")
    base_output = make_df("output", **base, node_dest=local, time_dest="year")

    return vintage_years, act_years,base_input, base_output

def transmission_S_SE(make_df,scenario):
    # Define the input and output link between S and SE
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # 1- Read the construction years and production years
    year_df = scenario.vintage_and_active_years()
    vintage_years, act_years = year_df["year_vtg"], year_df["year_act"]
    # 2- Create a basis class for input and output
    base_S_SE = dict(
        node_loc='S',
        year_vtg=vintage_years,
        year_act=act_years,
        mode="standard",
        time="year",
        unit="-",
    )
    base_S_SE_input = make_df("input", **base_S_SE, node_origin='S', time_origin="year")
    base_S_SE_output = make_df("output", **base_S_SE, node_dest='SE/CW', time_dest="year")

    # Power Transmission Technology (Secondary -> Secondary)
    grid_efficiency = 1
    grid_out = base_S_SE_output.assign(technology="transmission_S_SE/CW", commodity="electricity", level="secondary", value=grid_efficiency)
    grid_in  = base_S_SE_input.assign(technology="transmission_S_SE/CW", commodity="electricity", level="secondary", value=1.0)
    scenario.add_par("output", grid_out)
    scenario.add_par("input", grid_in)

    return scenario


def transmission_SE_S(make_df,scenario):
    # Define the input and output link between SE and S
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # 1- Read the construction years and production years
    year_df = scenario.vintage_and_active_years()
    vintage_years, act_years = year_df["year_vtg"], year_df["year_act"]
    # 2- Create a basis class for input and output
    base_SE_S = dict(
        node_loc='SE/CW',
        year_vtg=vintage_years,
        year_act=act_years,
        mode="standard",
        time="year",
        unit="-",
    )
    base_SE_S_input = make_df("input", **base_SE_S, node_origin='SE/CW', time_origin="year")
    base_SE_S_output = make_df("output", **base_SE_S, node_dest='S', time_dest="year")

    # Power Transmission Technology (Secondary -> Secondary)
    grid_efficiency = 1
    grid_out = base_SE_S_output.assign(technology="transmission_SE/CW_S", commodity="electricity", level="secondary", value=grid_efficiency)
    grid_in  = base_SE_S_input.assign(technology="transmission_SE/CW_S", commodity="electricity", level="secondary", value=1.0)
    scenario.add_par("output", grid_out)
    scenario.add_par("input", grid_in)

    return scenario


def transmission_SE_NE(make_df,scenario):
    # Define the input and output link between SE and NE
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # 1- Read the construction years and production years
    year_df = scenario.vintage_and_active_years()
    vintage_years, act_years = year_df["year_vtg"], year_df["year_act"]
    # 2- Create a basis class for input and output
    base_SE_NE = dict(
        node_loc='SE/CW',
        year_vtg=vintage_years,
        year_act=act_years,
        mode="standard",
        time="year",
        unit="-",
    )
    base_SE_NE_input = make_df("input", **base_SE_NE, node_origin='SE/CW', time_origin="year")
    base_SE_NE_output = make_df("output", **base_SE_NE, node_dest='NE', time_dest="year")

    # Power Transmission Technology (Secondary -> Secondary)
    grid_efficiency = 1
    grid_out = base_SE_NE_output.assign(technology="transmission_SE/CW_NE", commodity="electricity", level="secondary", value=grid_efficiency)
    grid_in  = base_SE_NE_input.assign(technology="transmission_SE/CW_NE", commodity="electricity", level="secondary", value=1.0)
    scenario.add_par("output", grid_out)
    scenario.add_par("input", grid_in)

    return scenario


def transmission_NE_SE(make_df,scenario):
    # Define the input and output link between NE and SE
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # 1- Read the construction years and production years
    year_df = scenario.vintage_and_active_years()
    vintage_years, act_years = year_df["year_vtg"], year_df["year_act"]
    # 2- Create a basis class for input and output
    base_NE_SE = dict(
        node_loc='NE',
        year_vtg=vintage_years,
        year_act=act_years,
        mode="standard",
        time="year",
        unit="-",
    )
    base_NE_SE_input = make_df("input", **base_NE_SE, node_origin='NE', time_origin="year")
    base_NE_SE_output = make_df("output", **base_NE_SE, node_dest='SE/CW', time_dest="year")

    # Power Transmission Technology (Secondary -> Secondary)
    grid_efficiency = 1
    grid_out = base_NE_SE_output.assign(technology="transmission_NE_SE/CW", commodity="electricity", level="secondary", value=grid_efficiency)
    grid_in  = base_NE_SE_input.assign(technology="transmission_NE_SE/CW", commodity="electricity", level="secondary", value=1.0)
    scenario.add_par("output", grid_out)
    scenario.add_par("input", grid_in)

    return scenario


def transmission_N_NE(make_df,scenario):
    # Define the input and output link between N and NE
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # 1- Read the construction years and production years
    year_df = scenario.vintage_and_active_years()
    vintage_years, act_years = year_df["year_vtg"], year_df["year_act"]
    # 2- Create a basis class for input and output
    base_N_NE = dict(
        node_loc='N',
        year_vtg=vintage_years,
        year_act=act_years,
        mode="standard",
        time="year",
        unit="-",
    )
    base_N_NE_input = make_df("input", **base_N_NE, node_origin='N', time_origin="year")
    base_N_NE_output = make_df("output", **base_N_NE, node_dest='NE', time_dest="year")

    # Power Transmission Technology (Secondary -> Secondary)
    grid_efficiency = 1
    grid_out = base_N_NE_output.assign(technology="transmission_N_NE", commodity="electricity", level="secondary", value=grid_efficiency)
    grid_in  = base_N_NE_input.assign(technology="transmission_N_NE", commodity="electricity", level="secondary", value=1.0)
    scenario.add_par("output", grid_out)
    scenario.add_par("input", grid_in)

    return scenario

def transmission_NE_N(make_df,scenario):
    # Define the input and output link between NE and N
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # 1- Read the construction years and production years
    year_df = scenario.vintage_and_active_years()
    vintage_years, act_years = year_df["year_vtg"], year_df["year_act"]
    # 2- Create a basis class for input and output
    base_NE_N = dict(
        node_loc='NE',
        year_vtg=vintage_years,
        year_act=act_years,
        mode="standard",
        time="year",
        unit="-",
    )
    base_NE_N_input = make_df("input", **base_NE_N, node_origin='NE', time_origin="year")
    base_NE_N_output = make_df("output", **base_NE_N, node_dest='N', time_dest="year")

    # Power Transmission Technology (Secondary -> Secondary)
    grid_efficiency = 1
    grid_out = base_NE_N_output.assign(technology="transmission_NE_N", commodity="electricity", level="secondary", value=grid_efficiency)
    grid_in  = base_NE_N_input.assign(technology="transmission_NE_N", commodity="electricity", level="secondary", value=1.0)
    scenario.add_par("output", grid_out)
    scenario.add_par("input", grid_in)

    return scenario


def transmission_N_SE(make_df,scenario):
    # Define the input and output link between N and SE
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # 1- Read the construction years and production years
    year_df = scenario.vintage_and_active_years()
    vintage_years, act_years = year_df["year_vtg"], year_df["year_act"]
    # 2- Create a basis class for input and output
    base_N_SE = dict(
        node_loc='N',
        year_vtg=vintage_years,
        year_act=act_years,
        mode="standard",
        time="year",
        unit="-",
    )
    base_N_SE_input = make_df("input", **base_N_SE, node_origin='N', time_origin="year")
    base_N_SE_output = make_df("output", **base_N_SE, node_dest='SE/CW', time_dest="year")

    # Power Transmission Technology (Secondary -> Secondary)
    grid_efficiency = 1
    grid_out = base_N_SE_output.assign(technology="transmission_N_SE/CW", commodity="electricity", level="secondary", value=grid_efficiency)
    grid_in  = base_N_SE_input.assign(technology="transmission_N_SE/CW", commodity="electricity", level="secondary", value=1.0)
    scenario.add_par("output", grid_out)
    scenario.add_par("input", grid_in)

    return scenario

def transmission_SE_N(make_df,scenario):
    # Define the input and output link between SE and N
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # 1- Read the construction years and production years
    year_df = scenario.vintage_and_active_years()
    vintage_years, act_years = year_df["year_vtg"], year_df["year_act"]
    # 2- Create a basis class for input and output
    base_SE_N = dict(
        node_loc='SE/CW',
        year_vtg=vintage_years,
        year_act=act_years,
        mode="standard",
        time="year",
        unit="-",
    )
    base_SE_N_input = make_df("input", **base_SE_N, node_origin='SE/CW', time_origin="year")
    base_SE_N_output = make_df("output", **base_SE_N, node_dest='N', time_dest="year")

    # Power Transmission Technology (Secondary -> Secondary)
    grid_efficiency = 1
    grid_out = base_SE_N_output.assign(technology="transmission_SE/CW_N", commodity="electricity", level="secondary", value=grid_efficiency)
    grid_in  = base_SE_N_input.assign(technology="transmission_SE/CW_N", commodity="electricity", level="secondary", value=1.0)
    scenario.add_par("output", grid_out)
    scenario.add_par("input", grid_in)

    return scenario

def technologies(scenario,base_input,base_output,local):
    
    # Define the connection of input and output of the technologies
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # Bulb Technology (Final -> Useful)
    bulb_out    = base_output.assign(technology="bulb_" + local, commodity="electric_households", level="useful", value=1.0)
    bulb_in     = base_input.assign(technology="bulb_" + local, commodity="electricity", level="final", value=1.0)
    scenario.add_par("output", bulb_out)
    scenario.add_par("input", bulb_in)
    scenario.idx_names("input")

    # Electricity Grid Technology (Secondary -> Final)
    grid_efficiency = 1
    grid_out = base_output.assign(technology="grid_" + local, commodity="electricity", level="final", value=grid_efficiency)
    grid_in  = base_input.assign(technology="grid_" + local, commodity="electricity", level="secondary", value=1.0)
    scenario.add_par("output", grid_out)
    scenario.add_par("input", grid_in)

    # Oil Generation ( ... -> Secondary)
    oil_out = base_output.assign(
        technology="oil_" + local + "_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", oil_out)

    # PCH Generation ( ... -> Secondary)
    pch_out = base_output.assign(
        technology="pch_" + local + "_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", pch_out)

    # Nuclear Generation ( ... -> Secondary)
    # Only for 'SE/CW'.
    if (local == 'SE/CW') or (local == 'NE'):
        nuclear_g_out = base_output.assign(
            technology="nuclear_g_" + local + "_ppl",
            commodity="electricity",
            level="secondary",
            value=1.0,
            unit="GWa",
        )
        scenario.add_par("output", nuclear_g_out)

    # Biogas Generation ( ... -> Secondary)
    biogas_out = base_output.assign(
        technology="biogas_" + local + "_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", biogas_out)

    # Solar Fotovoltaic Generation ( ... -> Secondary)
    solar_photovoltaic_out = base_output.assign(
        technology="solar_photovoltaic_" + local + "_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", solar_photovoltaic_out)

    # Solar CSP Generation ( ... -> Secondary)
    solar_csp_out = base_output.assign(
        technology="solar_csp_" + local + "_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", solar_csp_out)

    # Onshore Wind Generation ( ... -> Secondary)
    onshore_wind_out = base_output.assign(
        technology="onshore_wind_" + local + "_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", onshore_wind_out)

    # Offshore Wind Generation ( ... -> Secondary)
    offshore_wind_out = base_output.assign(
        technology="offshore_wind_" + local + "_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", offshore_wind_out)

    # Biomass Retrofit Generation ( ... -> Secondary)
    biomass_retrofit_out = base_output.assign(
        technology="biomass_retrofit_" + local + "_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", biomass_retrofit_out)

    # Onshore Wind Generation ( ... -> Secondary)
    biomass_greenfield_out = base_output.assign(
        technology="biomass_greenfield_" + local + "_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", biomass_greenfield_out)

    # NG Open Cycle Generation ( Secondary -> Secondary)
    GN_open_cycle_out = base_output.assign(
        technology="GN_open_cycle_" + local + "_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    GN_open_cycle_in_gnl = base_input.assign(
        technology="GN_open_cycle_" + local + "_ppl",
        commodity="gnl_imported",
        level="secondary",
        value=6.70,
        unit="MMm3/day",
    )
    GN_open_cycle_in_pipe = base_input.assign(
        technology="GN_open_cycle_" + local + "_ppl",
        commodity="natural_gas",
        level="secondary",
        value=6.70,
        unit="MMm3/day",
    )
    scenario.add_par("output", GN_open_cycle_out)
    scenario.add_par("input", GN_open_cycle_in_gnl)
    scenario.add_par("input", GN_open_cycle_in_pipe)
    scenario.idx_names("input")

    # NG Combined Cycle Generation ( Secondary -> Secondary)
    GN_combined_cycle_out = base_output.assign(
        technology="GN_combined_cycle_" + local + "_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    GN_combined_cycle_in_gnl = base_input.assign(
        technology="GN_combined_cycle_" + local + "_ppl",
        commodity="gnl_imported",
        level="secondary",
        value=4.26,
        unit="MMm3/day",
    )
    GN_combined_cycle_in_pipe = base_input.assign(
        technology="GN_combined_cycle_" + local + "_ppl",
        commodity="natural_gas",
        level="secondary",
        value=4.26,
        unit="MMm3/day",
    )
    scenario.add_par("output", GN_combined_cycle_out)
    scenario.add_par("input", GN_combined_cycle_in_gnl)
    scenario.add_par("input", GN_combined_cycle_in_pipe)

    # Large Hydroelectric Generation ( ... -> Secondary)
    large_hydroelectric_out = base_output.assign(
        technology="large_hydroelectric_" + local + "_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", large_hydroelectric_out)

    # Medium Hydroelectric Generation ( ... -> Secondary)
    medium_hydroelectric_out = base_output.assign(
        technology="medium_hydroelectric_" + local + "_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", medium_hydroelectric_out)

    # National Coal Generation ( ... -> Secondary)
    national_coal_out = base_output.assign(
        technology="national_coal_" + local + "_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", national_coal_out)

    # Imported Coal Generation ( ... -> Secondary)
    imported_coal_out = base_output.assign(
        technology="imported_coal_" + local + "_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", imported_coal_out)

    return scenario, grid_efficiency
