# Module of Connections on Technologies of Natural Gas (Input and Output)

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
    upgn_in    = base_input.assign(technology="UPGN", commodity="gas_extracted", level="primary", value=1.0)
    upgn_out    = base_output.assign(technology="UPGN", commodity="natural_gas", level="primary", value=1.0)
    scenario.add_par("input", upgn_in)
    scenario.add_par("output", upgn_out)

    #Gas Onshore (...-> Primary)
    onshore_out    = base_output.assign(technology="Gas_Onshore", commodity="gas_extracted", level="primary", value=1.0)
    scenario.add_par("output", onshore_out)


    #Gas Offshore (...-> Primary)
    if local != "N":
        offshore_out    = base_output.assign(technology="Gas_Offshore", commodity="gas_extracted", level="primary", value=1.0)
        scenario.add_par("output", offshore_out)

    #Reinjected Gas (Primary -> ...)
    if local != "N": 
        reinjection_in    = base_input.assign(technology="Gas_Reinjection", commodity="gas_extracted", level="primary", value=1.0)
        scenario.add_par("input", reinjection_in)
        scenario.idx_names("input")

    return scenario
