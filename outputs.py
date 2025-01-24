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


def validation_table(pd):
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

    for n in range(len(table.axes[1])-1):
    
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
                demand_north[i] = demand_north [i] + (float(table[table.axes[1][i+1]][j]))


        else:
            if "bulb_N" not in table["technology"][j] and "_NE" not in table["technology"][j] and "transmission" not in table["technology"][j] and "grid" not in table["technology"][j] and "_N_" in table["technology"][j]:
                for i in range(len(table.axes[1])-1):
                    act_north[i] = act_north [i] + (float(table[table.axes[1][i+1]][j]))

            elif "transmission" in table["technology"][j]:
                if "_N" in table["technology"][j]:
                    if "_N_" in table["technology"][j]:
                        for i in range(len(table.axes[1])-1):
                                transmission_north_out[i] = transmission_north_out[i] + (float(table[table.axes[1][i+1]][j]))

                    elif (table["technology"][j] == "transmission_SE/CW_N") or (table["technology"][j] == "transmission_NE_N"):
                        print(table["technology"][j])
                        for i in range(len(table.axes[1])-1):
                                transmission_north_in[i] = transmission_north_in[i] + (float(table[table.axes[1][i+1]][j]))

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


    values_n = {"North (values in GWa)": ["North Generation", "North Demand", "Difference", "Role", "Transmission leaves N", "Transmission joins N", "N total transmission", "Error (difference - transmission)", "Validated?"]}

    for p in range(len(table.axes[1])-1):
        values_n[table.axes[1][p+1]] = [act_north[p], demand_north[p], act_north[p]-demand_north[p], roles_n[p], transmission_north_out[p], transmission_north_in[p], transmission_north_out[p] - transmission_north_in[p], (((transmission_north_out[p]-transmission_north_in[p]) - (act_north[p] - demand_north[p]))), answers_n[p]]



    values_n = pd.DataFrame(values_n)

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

    for n in range(len(table.axes[1])-1):
    
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
                demand_northeast[i] = demand_northeast [i] + (float(table[table.axes[1][i+1]][j]))

        else:
            if "bulb" not in table["technology"][j] and "transmission" not in table["technology"][j] and "grid" not in table["technology"][j] and "_NE_" in table["technology"][j]:
                for i in range(len(table.axes[1])-1):
                    act_northeast[i] = act_northeast [i] + (float(table[table.axes[1][i+1]][j]))

            elif "transmission" in table["technology"][j]:
                if "_NE" in table["technology"][j]:
                    if "_NE_" in table["technology"][j]:
                        for i in range(len(table.axes[1])-1):
                            transmission_northeast_out[i] = transmission_northeast_out[i] + (float(table[table.axes[1][i+1]][j]))
                            
                    else:
                        for i in range(len(table.axes[1])-1):
                            transmission_northeast_in[i] = transmission_northeast_in[i] + (float(table[table.axes[1][i+1]][j]))

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


    values_ne = {"Northeast (values in GWa)": ["Northeast Generation", "Northeast Demand", "Difference", "Role", "Transmission leaves NE", "Transmission joins NE", "NE total transmission", "Error (difference - transmission)", "Validated?"]}

    for p in range(len(table.axes[1])-1):
        values_ne[table.axes[1][p+1]] = [act_northeast[p], demand_northeast[p], act_northeast[p]-demand_northeast[p], roles_ne[p], transmission_northeast_out[p], transmission_northeast_in[p], transmission_northeast_out[p] - transmission_northeast_in[p], (((transmission_northeast_out[p]-transmission_northeast_in[p]) - (act_northeast[p] - demand_northeast[p]))), answers_ne[p]]

    values_ne = pd.DataFrame(values_ne)

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

    for n in range(len(table.axes[1])-1):
    
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
                demand_southeast[i] = demand_southeast[i] + (float(table[table.axes[1][i+1]][j]))

        else:
            if "bulb" not in table["technology"][j] and "transmission" not in table["technology"][j] and "grid" not in table["technology"][j] and "_SE/CW_" in table["technology"][j]:
                for i in range(len(table.axes[1])-1):
                    act_southeast[i] = act_southeast[i] + (float(table[table.axes[1][i+1]][j]))

            elif "transmission" in table["technology"][j]:
                if "_SE/CW" in table["technology"][j]:
                    if "_SE/CW_" in table["technology"][j]:
                         for i in range(len(table.axes[1])-1):
                            transmission_southeast_out[i] = transmission_southeast_out[i] + (float(table[table.axes[1][i+1]][j]))
                    else:
                        for i in range(len(table.axes[1])-1):
                            transmission_southeast_in[i] = transmission_southeast_in[i] + (float(table[table.axes[1][i+1]][j]))

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


    values_se = {"Southeast (values in GWa)": ["Southeast Generation", "Southeast Demand", "Difference", "Role", "Transmission leaves SE", "Transmission joins SE", "SE total transmission", "Error (difference - transmission)", "Validated?"]}

    for p in range(len(table.axes[1])-1):
        values_se[table.axes[1][p+1]] = [act_southeast[p], demand_southeast[p], act_southeast[p]-demand_southeast[p], roles_se[p], transmission_southeast_out[p], transmission_southeast_in[p], transmission_southeast_out[p] - transmission_southeast_in[p], (((transmission_southeast_out[p]-transmission_southeast_in[p]) - (act_southeast[p] - demand_southeast[p]))), answers_se[p]]

    values_se = pd.DataFrame(values_se)


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

    for n in range(len(table.axes[1])-1):
    
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
                demand_south[i] = demand_south[i] + (float(table[table.axes[1][i+1]][j]))


        else:
            if "bulb" not in table["technology"][j] and "transmission" not in table["technology"][j] and "grid" not in table["technology"][j] and "_S_" in table["technology"][j]:
                for i in range(len(table.axes[1])-1):
                    act_south[i] = act_south[i] + (float(table[table.axes[1][i+1]][j]))

            elif "transmission" in table["technology"][j]:
                if "_S" in table["technology"][j]:
                    if "_S_" in table["technology"][j]:
                            for i in range(len(table.axes[1])-1):
                                transmission_south_out[i] = transmission_south_out[i] + (float(table[table.axes[1][i+1]][j]))
                                
                    elif "_SE/CW_S" in table["technology"][j]:
                            for i in range(len(table.axes[1])-1):
                                transmission_south_in[i] = transmission_south_in[i] + (float(table[table.axes[1][i+1]][j]))

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


    values_s = {"South (values in GWa)": ["South Generation", "South Demand", "Difference", "Role", "Transmission leaves S", "Transmission joins S", "S total transmission", "Error (difference - transmission)", "Validated?"]}

    for p in range(len(table.axes[1])-1):
        values_s[table.axes[1][p+1]] = [act_south[p], demand_south[p], act_south[p]-demand_south[p], roles_s[p], transmission_south_out[p], transmission_south_in[p], transmission_south_out[p] - transmission_south_in[p], (((transmission_south_out[p]-transmission_south_in[p]) - (act_south[p] - demand_south[p]))), answers_s[p]]

    values_s = pd.DataFrame(values_s)

    print(values_s)

    ###################

    return None
