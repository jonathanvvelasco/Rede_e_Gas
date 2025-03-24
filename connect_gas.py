# Module of Connections on Technologies of Natural Gas (Input and Output)

def technologies(scenario,base_input,base_output, local):
    
    # Define the connection of input and output of the technologies
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # Boiler (Secondary -> Useful)
    boiler_out    = base_output.assign(technology="boiler", commodity="gas_households", level="useful", value=1.0)
    boiler_in     = base_input.assign(technology="boiler", commodity="gas_distributed", level="secondary", value=1.0)
    scenario.add_par("output", boiler_out)
    scenario.add_par("input", boiler_in)

    # Gas Pipelines (...-> Secondary)
    pipe_out    = base_output.assign(technology="pipelines", commodity="gas_distributed", level="secondary", value=1.0)
    scenario.add_par("output", pipe_out)

    # Imported GNL (...-> Secondary)
    if local != "N":
        gnl_out    = base_output.assign(technology="GNL", commodity="gnl_imported", level="secondary", value=1.0)
        scenario.add_par("output", gnl_out)

    #GASBOL (...-> Primary)
    if local == "SE/CW":
        gasbol_out    = base_output.assign(technology="GASBOL", commodity="gas_bol", level="primary", value=1.0)
        scenario.add_par("output", gasbol_out)


    return scenario
