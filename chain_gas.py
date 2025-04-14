# Module of Technology Chain of Natural Gas (Input and Output)

def technologies(scenario,base_input,base_output, local):
    
    # Define the connection of input and output of the technologies
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # Boiler (Secondary -> Useful)
    boiler_out    = base_output.assign(technology="boiler", commodity="natural_gas", level="useful", value=1.0)
    boiler_in     = base_input.assign(technology="boiler", commodity="natural_gas", level="secondary", value=1.0)
    scenario.add_par("output", boiler_out)
    scenario.add_par("input", boiler_in)

    # Gas Pipelines (Primary -> Secondary)
    pipe_in    = base_input.assign(technology="pipelines", commodity="natural_gas", level="primary", value=1.0)
    pipe_out    = base_output.assign(technology="pipelines", commodity="natural_gas", level="secondary", value=1.0)
    scenario.add_par("input", pipe_in)
    scenario.add_par("output", pipe_out)

    # Imported GNL (...-> Secondary)
    if local != "N":
        gnl_out    = base_output.assign(technology="GNL", commodity="gnl_imported", level="secondary", value=1.0)
        scenario.add_par("output", gnl_out)

    #GASBOL (...-> Primary)
    if local == "SE/CW":
        gasbol_out    = base_output.assign(technology="GASBOL", commodity="natural_gas", level="primary", value=1.0)
        scenario.add_par("output", gasbol_out)

    #UPGN (Primary -> Primary)
    upgn_in     = base_input.assign(technology="UPGN", commodity="gas_extracted", level="primary", value=1.0)
    upgn_out    = base_output.assign(technology="UPGN", commodity="natural_gas", level="primary", value=1.0)
    scenario.add_par("input", upgn_in)
    scenario.add_par("output", upgn_out)

    #Gas Onshore (Resource -> Primary)
    onshore_in      = base_input.assign(technology="Gas_Onshore", commodity="gas_onland", level="resource", value=1.0)
    onshore_out     = base_output.assign(technology="Gas_Onshore", commodity="gas_extracted", level="primary", value=1.0)
    scenario.add_par("input", onshore_in)
    scenario.add_par("output", onshore_out)


    #Gas Offshore (...-> Primary)
    if (local != "N") and (local != "S"):
        offshore_in     = base_input.assign(technology="Gas_Offshore", commodity="gas_undersea", level="resource", value=1.0)
        offshore_out    = base_output.assign(technology="Gas_Offshore", commodity="gas_extracted", level="primary", value=1.0)
        scenario.add_par("input", offshore_in)
        scenario.add_par("output", offshore_out)

    #Reinjected Gas (Primary -> ...)
    if (local != "N") and (local != "S"): 
        reinjection_in    = base_input.assign(technology="Gas_Reinjection", commodity="gas_extracted", level="primary", value=1.0)
        scenario.add_par("input", reinjection_in)
        scenario.idx_names("input")

    return scenario

def gas_transport_S_SE(make_df,scenario):
    # Define the input and output link between S and SE
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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
    grid_out = base_S_SE_output.assign(technology="gas_transport_S_SE/CW", commodity="natural_gas", level="primary", value=grid_efficiency)
    grid_in  = base_S_SE_input.assign(technology="gas_transport_S_SE/CW", commodity="natural_gas", level="primary", value=1.0)
    scenario.add_par("output", grid_out)
    scenario.add_par("input", grid_in)

    return scenario

def gas_transport_SE_S(make_df,scenario):
    # Define the input and output link between S and SE
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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
    base_S_SE_input = make_df("input", **base_S_SE, node_origin='SE/CW', time_origin="year")
    base_S_SE_output = make_df("output", **base_S_SE, node_dest='S', time_dest="year")

    # Power Transmission Technology (Secondary -> Secondary)
    grid_efficiency = 1
    grid_out = base_S_SE_output.assign(technology="gas_transport_SE/CW_S", commodity="natural_gas", level="primary", value=grid_efficiency)
    grid_in  = base_S_SE_input.assign(technology="gas_transport_SE/CW_S", commodity="natural_gas", level="primary", value=1.0)
    scenario.add_par("output", grid_out)
    scenario.add_par("input", grid_in)

    return scenario