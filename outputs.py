# Module Outputs

def generate_excel(pd,scenario):
    # Create Excel outputs
    # ^^^^^^^^^^^^^^^^^

    b = pd.DataFrame(scenario.var("CAP"))
    b.to_excel("Capacity.xlsx")
    
    c = pd.DataFrame(scenario.var("CAP_NEW"))
    c.to_excel("New Capacity.xlsx")

    d = pd.DataFrame(scenario.var("ACT")).pivot_table(index="technology", columns="year_act", values="lvl", aggfunc="sum")
    d.to_excel("Activity.xlsx")

    return None



def validation_table(pd, scenario, historic_demand_N, historic_demand_NE, historic_demand_S, historic_demand_SW, historic_act_N, historic_act_NE, historic_act_S, historic_act_SW, history, model_horizon):
    ###Demand and supply table###


    table = pd.read_excel("Activity.xlsx")

    #############################
    

    ############North############


    ###Creating lists###

    demand_north = []
    act_north= []
    transmission_north_in = []
    transmission_north_out = []
    roles_n = []
    answers_n = []

    for n in range(len(historic_demand_N) + len(table.axes[1])-1):

        if n < len(historic_demand_N):
            demand_north.append(historic_demand_N[n])
            act_north.append(sum(historic_act_N[n]))
            transmission_north_in.append(0)
            transmission_north_out.append(0)
            roles_n.append("")
            answers_n.append("")

        else:
        
            demand_north.append(0)
            act_north.append(0)
            transmission_north_in.append(0)
            transmission_north_out.append(0)
            roles_n.append("")
            answers_n.append("")

    ####################

    
    for j in range(len(table["technology"])):
        if "bulb_N" in table["technology"][j] and "_NE" not in table["technology"][j]:
            for i in range(len(table.axes[1])-1):
                demand_north[i + len(historic_demand_N)] = demand_north [i + len(historic_demand_N)] + (float(table[table.axes[1][i+1]][j]))


        else:
            if "bulb_N" not in table["technology"][j] and "_NE" not in table["technology"][j] and "transmission" not in table["technology"][j] and "grid" not in table["technology"][j] and "_N_" in table["technology"][j]:
                for i in range(len(table.axes[1])-1):
                    act_north[i + len(historic_demand_N)] = act_north [i + len(historic_demand_N)] + (float(table[table.axes[1][i+1]][j]))

            elif "transmission" in table["technology"][j]:
                if "_N" in table["technology"][j]:
                    if "_N_" in table["technology"][j]:
                        for i in range(len(table.axes[1])-1):
                                transmission_north_out[i + len(historic_demand_N)] = transmission_north_out[i + len(historic_demand_N)] + (float(table[table.axes[1][i+1]][j]))

                    elif (table["technology"][j] == "transmission_SE/CW_N") or (table["technology"][j] == "transmission_NE_N"):
                        for i in range(len(table.axes[1])-1):
                                transmission_north_in[i + len(historic_demand_N)] = transmission_north_in[i + len(historic_demand_N)] + (float(table[table.axes[1][i+1]][j]))

    ###Roles###
                            

    for j in range(len(roles_n)):
        if act_north[j]-demand_north[j] > 0:
            roles_n[j] = "Exporter"
        else:
            roles_n[j] = "Importer"


    ###Validation###

            
        if (abs((transmission_north_out[j]-transmission_north_in[j]) - (act_north[j] - demand_north[j]))) < 10**(-5):
            answers_n[j] = "Yes"
        else:
            answers_n[j] = "No"


    ################
            



    #creating the table


    values_n = {"North (values in GWa)": ["Years", "North Generation", "North Demand", "Difference", "Role", "Transmission leaves N", "Transmission joins N", "N total transmission", "Error (difference - transmission)", "Validated?"]}
    for p in range(len(demand_north)):
        if p < len(historic_demand_N):
            values_n[p] = [history[p], act_north[p], demand_north[p], act_north[p]-demand_north[p], roles_n[p], "-", "-", "-", "-", "-"]
        else:
            values_n[p] = [model_horizon[p-len(history)], act_north[p], demand_north[p], act_north[p]-demand_north[p], roles_n[p], transmission_north_out[p], transmission_north_in[p], transmission_north_out[p] - transmission_north_in[p], (((transmission_north_out[p]-transmission_north_in[p]) - (act_north[p] - demand_north[p]))), answers_n[p]]



    values_n = pd.DataFrame(values_n)
    values_n = values_n.to_string(index=False, header=False)
    
    print("                       North")
    print(values_n)
    print("")


    ###################







    ########################################







    ############Northeast############

    ###Creating lists###

    demand_northeast = []
    act_northeast = []
    transmission_northeast_in = []
    transmission_northeast_out = []
    roles_ne = []
    answers_ne = []

    for n in range(len(historic_demand_NE) + len(table.axes[1])-1):

        if n < len(historic_demand_NE):
            demand_northeast.append(historic_demand_NE[n])
            act_northeast.append(sum(historic_act_NE[n]))
            transmission_northeast_in.append(0)
            transmission_northeast_out.append(0)
            roles_ne.append("")
            answers_ne.append("")

        else:
        
            demand_northeast.append(0)
            act_northeast.append(0)
            transmission_northeast_in.append(0)
            transmission_northeast_out.append(0)
            roles_ne.append("")
            answers_ne.append("")

    ####################


    for j in range(len(table["technology"])):
        if "bulb_NE" in table["technology"][j]:
            for i in range(len(table.axes[1])-1):
                demand_northeast[i + len(historic_demand_NE)] = demand_northeast [i + len(historic_demand_NE)] + (float(table[table.axes[1][i+1]][j]))

        else:
            if "bulb" not in table["technology"][j] and "transmission" not in table["technology"][j] and "grid" not in table["technology"][j] and "_NE_" in table["technology"][j]:
                for i in range(len(table.axes[1])-1):
                    act_northeast[i + len(historic_demand_NE)] = act_northeast [i + len(historic_demand_NE)] + (float(table[table.axes[1][i+1]][j]))

            elif "transmission" in table["technology"][j]:
                if "_NE" in table["technology"][j]:
                    if "_NE_" in table["technology"][j]:
                        for i in range(len(table.axes[1])-1):
                            transmission_northeast_out[i + len(historic_demand_NE)] = transmission_northeast_out[i + len(historic_demand_NE)] + (float(table[table.axes[1][i+1]][j]))
                            
                    else:
                        for i in range(len(table.axes[1])-1):
                            transmission_northeast_in[i + len(historic_demand_NE)] = transmission_northeast_in[i + len(historic_demand_NE)] + (float(table[table.axes[1][i+1]][j]))

    ###Roles###

    for j in range(len(roles_ne)):
        if act_northeast[j]-demand_northeast[j] > 0:
            roles_ne[j] = "Exporter"
        else:
            roles_ne[j] = "Importer"


    ###Validation###

            
        if (abs((transmission_northeast_out[j]-transmission_northeast_in[j]) - (act_northeast[j] - demand_northeast[j]))) < 10**(-5):
            answers_ne[j] = "Yes"
        else:
            answers_ne[j] = "No"


    ################

            
    #creating the table


    values_ne = {"Northeast (values in GWa)": ["Years", "Northeast Generation", "Northeast Demand", "Difference", "Role", "Transmission leaves NE", "Transmission joins NE", "NE total transmission", "Error (difference - transmission)", "Validated?"]}

    for p in range(len(demand_northeast)):
        if p < len(historic_demand_N):
            values_ne[p] = [history[p], act_northeast[p], demand_northeast[p], act_northeast[p]-demand_northeast[p], roles_ne[p], "-", "-", "-", "-", "-"]
        else:
            values_ne[p] = [model_horizon[p-len(history)], act_northeast[p], demand_northeast[p], act_northeast[p]-demand_northeast[p], roles_ne[p], transmission_northeast_out[p], transmission_northeast_in[p], transmission_northeast_out[p] - transmission_northeast_in[p], (((transmission_northeast_out[p]-transmission_northeast_in[p]) - (act_northeast[p] - demand_northeast[p]))), answers_ne[p]]
            
    values_ne = pd.DataFrame(values_ne)
    values_ne = values_ne.to_string(index=False, header=False)
    
    print("                   Northeast")
    print(values_ne)
    print("")


    ###################






    ########################################





    ############Southeast############
    

    ###Creating lists###

    demand_southeast = []
    act_southeast = []
    transmission_southeast_in = []
    transmission_southeast_out = []
    roles_se = []
    answers_se = []

    for n in range(len(historic_demand_SW) + len(table.axes[1])-1):

        if n < len(historic_demand_SW):
            demand_southeast.append(historic_demand_SW[n])
            act_southeast.append(sum(historic_act_SW[n]))
            transmission_southeast_in.append(0)
            transmission_southeast_out.append(0)
            roles_se.append("")
            answers_se.append("")

        else:
        
            demand_southeast.append(0)
            act_southeast.append(0)
            transmission_southeast_in.append(0)
            transmission_southeast_out.append(0)
            roles_se.append("")
            answers_se.append("")

    ####################


    for j in range(len(table["technology"])):
        if "bulb_SE/CW" in table["technology"][j]:
            for i in range(len(table.axes[1])-1):
                demand_southeast[i + len(historic_demand_SW)] = demand_southeast[i + len(historic_demand_SW)] + (float(table[table.axes[1][i+1]][j]))

        else:
            if "bulb" not in table["technology"][j] and "transmission" not in table["technology"][j] and "grid" not in table["technology"][j] and "_SE/CW_" in table["technology"][j]:
                for i in range(len(table.axes[1])-1):
                    act_southeast[i + len(historic_demand_SW)] = act_southeast[i + len(historic_demand_SW)] + (float(table[table.axes[1][i+1]][j]))

            elif "transmission" in table["technology"][j]:
                if "_SE/CW" in table["technology"][j]:
                    if "_SE/CW_" in table["technology"][j]:
                         for i in range(len(table.axes[1])-1):
                            transmission_southeast_out[i + len(historic_demand_SW)] = transmission_southeast_out[i + len(historic_demand_SW)] + (float(table[table.axes[1][i+1]][j]))
                    else:
                        for i in range(len(table.axes[1])-1):
                            transmission_southeast_in[i + len(historic_demand_SW)] = transmission_southeast_in[i + len(historic_demand_SW)] + (float(table[table.axes[1][i+1]][j]))

    ###Roles###
                            

    for j in range(len(roles_se)):
        if act_southeast[j]-demand_southeast[j] > 0:
            roles_se[j] = "Exporter"
        else:
            roles_se[j] = "Importer"


    ###Validation###

            
        if (abs((transmission_southeast_out[j]-transmission_southeast_in[j]) - (act_southeast[j] - demand_southeast[j]))) < 10**(-5):
            answers_se[j] = "Yes"
        else:
            answers_se[j] = "No"


    ################

            
    #creating the table


    values_se = {"Southeast (values in GWa)": ["Years", "Southeast Generation", "Southeast Demand", "Difference", "Role", "Transmission leaves SE", "Transmission joins SE", "SE total transmission", "Error (difference - transmission)", "Validated?"]}

    for p in range(len(demand_southeast)):
        if p < len(historic_demand_SW):
            values_se[p] = [history[p], act_southeast[p], demand_southeast[p], act_southeast[p]-demand_southeast[p], roles_se[p], "-", "-", "-", "-", "-"]
        else:
            values_se[p] = [model_horizon[p-len(history)], act_southeast[p], demand_southeast[p], act_southeast[p]-demand_southeast[p], roles_se[p], transmission_southeast_out[p], transmission_southeast_in[p], transmission_southeast_out[p] - transmission_southeast_in[p], (((transmission_southeast_out[p]-transmission_southeast_in[p]) - (act_southeast[p] - demand_southeast[p]))), answers_se[p]]

    values_se = pd.DataFrame(values_se)
    values_se = values_se.to_string(index=False, header=False)
    
    print("                   Southeast")
    print(values_se)
    print("")

    ###################



    ############South############


    ###Creating lists###

    demand_south = []
    act_south = []
    transmission_south_in = []
    transmission_south_out = []
    roles_s = []
    answers_s = []

    for n in range(len(historic_demand_S) + len(table.axes[1])-1):

        if n < len(historic_demand_S):
            demand_south.append(historic_demand_S[n])
            act_south.append(sum(historic_act_S[n]))
            transmission_south_in.append(0)
            transmission_south_out.append(0)
            roles_s.append("")
            answers_s.append("")

        else:
        
            demand_south.append(0)
            act_south.append(0)
            transmission_south_in.append(0)
            transmission_south_out.append(0)
            roles_s.append("")
            answers_s.append("")

    ####################



    for j in range(len(table["technology"])):
        if "bulb_S" == table["technology"][j]:
            for i in range(len(table.axes[1])-1):
                demand_south[i + len(historic_demand_S)] = demand_south[i + len(historic_demand_S)] + (float(table[table.axes[1][i+1]][j]))


        else:
            if "bulb" not in table["technology"][j] and "transmission" not in table["technology"][j] and "grid" not in table["technology"][j] and "_S_" in table["technology"][j]:
                for i in range(len(table.axes[1])-1):
                    act_south[i + len(historic_demand_S)] = act_south[i + len(historic_demand_S)] + (float(table[table.axes[1][i+1]][j]))

            elif "transmission" in table["technology"][j]:
                if "_S" in table["technology"][j]:
                    if "_S_" in table["technology"][j]:
                            for i in range(len(table.axes[1])-1):
                                transmission_south_out[i + len(historic_demand_S)] = transmission_south_out[i] + (float(table[table.axes[1][i+1]][j]))
                                
                    elif "_SE/CW_S" in table["technology"][j]:
                            for i in range(len(table.axes[1])-1):
                                transmission_south_in[i + len(historic_demand_S)] = transmission_south_in[i + len(historic_demand_S)] + (float(table[table.axes[1][i+1]][j]))

    ###Roles###
                            

    for j in range(len(roles_s)):
        if act_south[j]-demand_south[j] > 0:
            roles_s[j] = "Exporter"
        else:
            roles_s[j] = "Importer"


    ###Validation###

            
        if (abs((transmission_south_out[j]-transmission_south_in[j]) - (act_south[j] - demand_south[j]))) < 10**(-5):
            answers_s[j] = "Yes"
        else:
            answers_s[j] = "No"


    ################

            
    #creating the table


    values_s = {"South (values in GWa)": ["Years", "South Generation", "South Demand", "Difference", "Role", "Transmission leaves S", "Transmission joins S", "S total transmission", "Error (difference - transmission)", "Validated?"]}

    for p in range(len(demand_south)):
        if p < len(historic_demand_S):
            values_s[p] = [history[p], act_south[p], demand_south[p], act_south[p]-demand_south[p], roles_s[p], "-", "-", "-", "-", "-"]
        else:
            values_s[p] = [model_horizon[p-len(history)], act_south[p], demand_south[p], act_south[p]-demand_south[p], roles_s[p], transmission_south_out[p], transmission_south_in[p], transmission_south_out[p] - transmission_south_in[p], (((transmission_south_out[p]-transmission_south_in[p]) - (act_south[p] - demand_south[p]))), answers_s[p]]

    values_s = pd.DataFrame(values_s)
    values_s = values_s.to_string(index=False, header=False)
    
    print("                       South")
    print(values_s)

    #creating the excel with the historical years
    d = pd.DataFrame(scenario.var("ACT"))
    d.to_excel("Activity.xlsx")
    

    ###################
    

    return None


def plots(scenario, Reporter, prepare_plots, plt):
    #creating the plots
    rep = Reporter.from_scenario(scenario)
    prepare_plots(rep)

    ###################

    #activity
    # rep.get("plot activity")
    # plt.title("Energy System Activity")

    ###################

    #new capacity
    tol = 1e-3                                                      # Tolerância para gráfico
    keyCAP_NEW = rep.full_key("CAP_NEW")                            # Chave CAP_NEW
    dfCAP_NEW  = rep.get(keyCAP_NEW)                                # Dados CAP_NEW
    dados_EXP  = dfCAP_NEW[dfCAP_NEW>tol]                           # Filtra CAP_NEW >tol
    tecno_EXP  = dados_EXP.index.get_level_values('t').tolist()     # Lista Tecnologias em Expansão
    tecno_EXP  = list(set(tecno_EXP))                               # Remove duplicatas
    tecno_EXP = [item for item in tecno_EXP if not item.startswith('bulb')]  # Remove bulb

    rep.set_filters(t=tecno_EXP)                                # Filtra tecnologias
    rep.get("plot new capacity")                                # Plota gráfico
    plt.title("Energy System New Capacity")

    # Teste futuro
    # dados_EXP1 = dados_EXP[~dados_EXP.index.get_level_values('t').str.startswith('bulb')]
    # dados_EXP1.plot(kind='bar',title="Energy System New Capacity", stacked=True, legend=True)

    ###################

    #showing the graphs
    plt.show()
    
    ##########
    return None

def sankey(scenario,Reporter):
    from genno.operator import concat
    from message_ix.tools.sankey import map_for_sankey
    from pyam.figures import sankey
    
    # Inputs
    subsystems = ['N','NE','SE/CW','S']
    annum = [2025]

    for subsystem in subsystems:
        # Create Sankey diagram for each subsystem
        rep = Reporter.from_scenario(scenario, units={"replace": {"-": ""}}) # Remove "-" from units
        df_all = concat(rep.get("in::pyam"), rep.get("out::pyam"))           # Concatenate input and output dataframes
        df = df_all.filter(year=annum, region=subsystem+'|'+subsystem)       # Filter for the year and subsystem
        mapping = map_for_sankey(df, node=subsystem,)                        # Map the data for Sankey diagram
        fig = sankey(df=df, mapping=mapping)                                 # Create the Sankey diagram
        fig.show()

    return None