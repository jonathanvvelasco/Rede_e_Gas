import pandas as pd
import ixmp
import message_ix
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
from tkinter import messagebox
import tkinter as tk

from message_ix.utils import make_df

import begin
import connect
import describe
import limits
import outputs


mp = ixmp.Platform()
mp.add_unit("USD/MWh")
mp.add_unit("USD/kW-a")


scenario = message_ix.Scenario(mp, model="Brazil Electrified", scenario="baseline", version="new")


scenario, history, model_horizon, country, nodes    = begin.definitions (pd,scenario)

for local in nodes:
    scenario                                            = begin.demand    (pd,scenario,model_horizon,local)
    vintage_years, act_years,base_input, base_output    = connect.base         (make_df,scenario,local)
    scenario, grid_efficiency                           = connect.technologies  (scenario,base_input, base_output,local)
    scenario, capacity_factor               = describe.capacity__factor     (make_df,scenario,local,vintage_years, act_years)
    scenario                                = describe.life_time            (make_df,scenario,local,model_horizon)
    scenario                                = describe.growth__tecnologies  (make_df,scenario,local,model_horizon)
    scenario                                = describe.historic__generation    (make_df,scenario,grid_efficiency,local,history,capacity_factor)
    scenario                                = describe.inv_costs   (make_df,scenario,local,model_horizon)
    scenario                                = describe.fix_costs           (make_df,scenario,local,vintage_years, act_years)
    scenario                                = describe.var_costs       (make_df,scenario,local,vintage_years, act_years)
    scenario                                = limits.expansion_up           (make_df,scenario,local)

scenario = connect.transmission_S_SE(make_df,scenario)
scenario = connect.transmission_SE_S(make_df,scenario)
scenario = connect.transmission_SE_NE(make_df,scenario)
scenario = connect.transmission_NE_SE(make_df,scenario)
scenario = connect.transmission_N_NE(make_df,scenario)
scenario = connect.transmission_NE_N(make_df,scenario)
scenario = connect.transmission_N_SE(make_df,scenario)
scenario = connect.transmission_SE_N(make_df,scenario)


scenario.solve()






##outputs.generate_excel(pd,scenario)

##tk.messagebox.showinfo("Notification", "The code has been successfully run!")



###Demand and supply table###


table = pd.read_excel("Activity.xlsx")

#############################


############North############

demand_north = [0,0,0]
act_north = [0,0,0]
transmission_north_in = [0,0,0]
transmission_north_out = [0,0,0]
roles_n = ["", "", ""]
answers_n = ["", "", ""]



for j in range(len(table["technology"])):
    if "bulb_N" in table["technology"][j] and "_NE" not in table["technology"][j]:
        demand_north[0] = demand_north [0] + (float(table[2015][j]))
        demand_north[1] = demand_north [1] + float(table[2020][j])
        demand_north[2] = demand_north [2] + float(table[2025][j])

    else:
        if "bulb_N" not in table["technology"][j] and "_NE" not in table["technology"][j] and "transmission" not in table["technology"][j] and "grid" not in table["technology"][j] and "_N_" in table["technology"][j]:
            act_north[0] = act_north[0] + float(table[2015][j])
            act_north[1] = act_north[1] + float(table[2020][j])
            act_north[2] = act_north[2] + float(table[2025][j])

        elif "transmission" in table["technology"][j]:
            if "_N" in table["technology"][j]:
                if "_N_" in table["technology"][j]:
                        transmission_north_out[0] = transmission_north_out[0] + float(table[2015][j])
                        transmission_north_out[1] = transmission_north_out[1] + float(table[2020][j])
                        transmission_north_out[2] = transmission_north_out[2] + float(table[2025][j])
                elif ("SE/CW_N" in table["technology"][j] and "NE" not in table["technology"][j]) or ("NE_N" not in table["technology"][j]):
                        transmission_north_in[0] = transmission_north_in[0] + float(table[2015][j])
                        transmission_north_in[1] = transmission_north_in[1] + float(table[2020][j])
                        transmission_north_in[2] = transmission_north_in[2] + float(table[2025][j])

###Roles###
                        

for j in range(len(roles_n)):
    if act_north[j]-demand_north[j] > 0:
        roles_n[j] = "Exporter"
    else:
        roles_n[j] = "Importer"


###Validation###

        
    if (float((transmission_north_out[j]-transmission_north_in[j]) - (act_north[j] - demand_north[j]))) < 10**(-5):
        answers_n[j] = "Yes"
    else:
        answers_n[j] = "No"



################
        



#creating the table


values_n = {"North (values in GWa)": ["North Generation", "North Demand", "Difference", "Role", "Transmission leaves N", "Transmission joins N", "N total transmission", "Error (difference - transmission)", "Validated?"],
              "2015": [act_north[0], demand_north[0], act_north[0]-demand_north[0], roles_n[0], transmission_north_out[0], transmission_north_in[0], transmission_north_out[0] - transmission_north_in[0], (((transmission_north_out[0]-transmission_north_in[0]) - (act_north[0] - demand_north[0]))), answers_n[0]],
              "2020": [act_north[1], demand_north[1], act_north[1]-demand_north[1], roles_n[1], transmission_north_out[1], transmission_north_in[1], transmission_north_out[1] - transmission_north_in[1], (((transmission_north_out[1]-transmission_north_in[1]) - (act_north[1] - demand_north[1]))), answers_n[1]],        
              "2025": [act_north[2], demand_north[2], act_north[2]-demand_north[2], roles_n[2], transmission_north_out[2], transmission_north_in[2], transmission_north_out[2] - transmission_north_in[2], (((transmission_north_out[2]-transmission_north_in[2]) - (act_north[2] - demand_north[2]))), answers_n[2]]}


values_n = pd.DataFrame(values_n)

print(values_n)


###################







########################################







############Northeast############

demand_northeast = [0,0,0]
act_northeast = [0,0,0]
transmission_northeast_in = [0,0,0]
transmission_northeast_out = [0,0,0]
roles_ne = ["", "", ""]
answers_ne = ["", "", ""]



for j in range(len(table["technology"])):
    if "bulb_NE" in table["technology"][j]:
        demand_northeast[0] = demand_northeast [0] + (float(table[2015][j]))
        demand_northeast[1] = demand_northeast [1] + float(table[2020][j])
        demand_northeast[2] = demand_northeast [2] + float(table[2025][j])

    else:
        if "bulb" not in table["technology"][j] and "transmission" not in table["technology"][j] and "grid" not in table["technology"][j] and "_NE_" in table["technology"][j]:
            act_northeast[0] = act_northeast[0] + float(table[2015][j])
            act_northeast[1] = act_northeast[1] + float(table[2020][j])
            act_northeast[2] = act_northeast[2] + float(table[2025][j])

        elif "transmission" in table["technology"][j]:
            if "_NE" in table["technology"][j]:
                if "_NE_" in table["technology"][j]:
                        transmission_northeast_out[0] = transmission_northeast_out[0] + float(table[2015][j])
                        transmission_northeast_out[1] = transmission_northeast_out[1] + float(table[2020][j])
                        transmission_northeast_out[2] = transmission_northeast_out[2] + float(table[2025][j])
                else:
                        transmission_northeast_in[0] = transmission_northeast_in[0] + float(table[2015][j])
                        transmission_northeast_in[1] = transmission_northeast_in[1] + float(table[2020][j])
                        transmission_northeast_in[2] = transmission_northeast_in[2] + float(table[2025][j])

###Roles###
                        

for j in range(len(roles_ne)):
    if act_northeast[j]-demand_northeast[j] > 0:
        roles_ne[j] = "Exporter"
    else:
        roles_ne[j] = "Importer"


###Validation###

        
    if (float((transmission_northeast_out[j]-transmission_northeast_in[j]) - (act_northeast[j] - demand_northeast[j]))) < 10**(-5):
        answers_ne[j] = "Yes"
    else:
        answers_ne[j] = "No"


################

        
#creating the table


values_ne = {"Northeast (values in GWa)": ["Northeast Generation", "Northeast Demand", "Difference", "Role", "Transmission leaves NE", "Transmission joins NE", "NE total transmission", "Error (difference - transmission)", "Validated?"],
              "2015": [act_northeast[0], demand_northeast[0], act_northeast[0]-demand_northeast[0], roles_ne[0], transmission_northeast_out[0], transmission_northeast_in[0], transmission_northeast_out[0] - transmission_northeast_in[0], (((transmission_northeast_out[0]-transmission_northeast_in[0]) - (act_northeast[0] - demand_northeast[0]))), answers_ne[0]],
              "2020": [act_northeast[1], demand_northeast[1], act_northeast[1]-demand_northeast[1], roles_ne[1], transmission_northeast_out[1], transmission_northeast_in[1], transmission_northeast_out[1] - transmission_northeast_in[1], (((transmission_northeast_out[1]-transmission_northeast_in[1]) - (act_northeast[1] - demand_northeast[1]))), answers_ne[1]],        
              "2025": [act_northeast[2], demand_northeast[2], act_northeast[2]-demand_northeast[2], roles_ne[2], transmission_northeast_out[2], transmission_northeast_in[2], transmission_northeast_out[2] - transmission_northeast_in[2], (((transmission_northeast_out[2]-transmission_northeast_in[2]) - (act_northeast[2] - demand_northeast[2]))), answers_ne[2]]}

values_ne = pd.DataFrame(values_ne)

print(values_ne)


###################






########################################





############Southeast############


demand_southeast = [0,0,0]
act_southeast = [0,0,0]
transmission_southeast_in = [0,0,0]
transmission_southeast_out = [0,0,0]
roles_se = ["", "", ""]
answers_se = ["", "", ""]



for j in range(len(table["technology"])):
    if "bulb_SE/CW" in table["technology"][j]:
        demand_southeast[0] = demand_southeast [0] + (float(table[2015][j]))
        demand_southeast[1] = demand_southeast [1] + float(table[2020][j])
        demand_southeast[2] = demand_southeast [2] + float(table[2025][j])

    else:
        if "bulb" not in table["technology"][j] and "transmission" not in table["technology"][j] and "grid" not in table["technology"][j] and "_SE/CW_" in table["technology"][j]:
            act_southeast[0] = act_southeast[0] + float(table[2015][j])
            act_southeast[1] = act_southeast[1] + float(table[2020][j])
            act_southeast[2] = act_southeast[2] + float(table[2025][j])

        elif "transmission" in table["technology"][j]:
            if "_SE/CW" in table["technology"][j]:
                if "_SE/CW_" in table["technology"][j]:
                        transmission_southeast_out[0] = transmission_southeast_out[0] + float(table[2015][j])
                        transmission_southeast_out[1] = transmission_southeast_out[1] + float(table[2020][j])
                        transmission_southeast_out[2] = transmission_southeast_out[2] + float(table[2025][j])
                else:
                        transmission_southeast_in[0] = transmission_southeast_in[0] + float(table[2015][j])
                        transmission_southeast_in[1] = transmission_southeast_in[1] + float(table[2020][j])
                        transmission_southeast_in[2] = transmission_southeast_in[2] + float(table[2025][j])

###Roles###
                        

for j in range(len(roles_se)):
    if act_southeast[j]-demand_southeast[j] > 0:
        roles_se[j] = "Exporter"
    else:
        roles_se[j] = "Importer"


###Validation###

        
    if (float((transmission_southeast_out[j]-transmission_southeast_in[j]) - (act_southeast[j] - demand_southeast[j]))) < 10**(-5):
        answers_se[j] = "Yes"
    else:
        answers_se[j] = "No"


################

        
#creating the table


values_se = {"Southeast (values in GWa)": ["Southeast Generation", "Southeast Demand", "Difference", "Role", "Transmission leaves SE", "Transmission joins SE", "SE total transmission", "Error (difference - transmission)", "Validated?"],
              "2015": [act_southeast[0], demand_southeast[0], act_southeast[0]-demand_southeast[0], roles_se[0], transmission_southeast_out[0], transmission_southeast_in[0], transmission_southeast_out[0] - transmission_southeast_in[0], (((transmission_southeast_out[0]-transmission_southeast_in[0]) - (act_southeast[0] - demand_southeast[0]))), answers_se[0]],
              "2020": [act_southeast[1], demand_southeast[1], act_southeast[1]-demand_southeast[1], roles_se[1], transmission_southeast_out[1], transmission_southeast_in[1], transmission_southeast_out[1] - transmission_southeast_in[1], (((transmission_southeast_out[1]-transmission_southeast_in[1]) - (act_southeast[1] - demand_southeast[1]))), answers_se[1]],        
              "2025": [act_southeast[2], demand_southeast[2], act_southeast[2]-demand_southeast[2], roles_se[2], transmission_southeast_out[2], transmission_southeast_in[2], transmission_southeast_out[2] - transmission_southeast_in[2], (((transmission_southeast_out[2]-transmission_southeast_in[2]) - (act_southeast[2] - demand_southeast[2]))), answers_se[2]]}

values_se = pd.DataFrame(values_se)

print(values_se)

###################



############South############



demand_south = [0,0,0]
act_south = [0,0,0]
transmission_south_in = [0,0,0]
transmission_south_out = [0,0,0]
roles_s = ["", "", ""]
answers_s = ["", "", ""]



for j in range(len(table["technology"])):
    if "bulb_S" == table["technology"][j]:
        demand_south[0] = demand_south [0] + (float(table[2015][j]))
        demand_south[1] = demand_south[1] + float(table[2020][j])
        demand_south[2] = demand_south [2] + float(table[2025][j])

    else:
        if "bulb" not in table["technology"][j] and "transmission" not in table["technology"][j] and "grid" not in table["technology"][j] and "_S_" in table["technology"][j]:
            act_south[0] = act_south[0] + float(table[2015][j])
            act_south[1] = act_south[1] + float(table[2020][j])
            act_south[2] = act_south[2] + float(table[2025][j])

        elif "transmission" in table["technology"][j]:
            if "_S" in table["technology"][j]:
                if "_S_" in table["technology"][j]:
                        transmission_south_out[0] = transmission_south_out[0] + float(table[2015][j])
                        transmission_south_out[1] = transmission_south_out[1] + float(table[2020][j])
                        transmission_south_out[2] = transmission_south_out[2] + float(table[2025][j])
                elif "_SE/CW_S" in table["technology"][j]:
                        transmission_south_in[0] = transmission_south_in[0] + float(table[2015][j])
                        transmission_south_in[1] = transmission_south_in[1] + float(table[2020][j])
                        transmission_south_in[2] = transmission_south_in[2] + float(table[2025][j])

###Roles###
                        

for j in range(len(roles_s)):
    if act_south[j]-demand_south[j] > 0:
        roles_s[j] = "Exporter"
    else:
        roles_s[j] = "Importer"


###Validation###

        
    if (float((transmission_south_out[j]-transmission_south_in[j]) - (act_south[j] - demand_south[j]))) < 10**(-5):
        answers_s[j] = "Yes"
    else:
        answers_s[j] = "No"


################

        
#creating the table


values_s = {"South (values in GWa)": ["South Generation", "South Demand", "Difference", "Role", "Transmission leaves S", "Transmission joins S", "S total transmission", "Error (difference - transmission)", "Validated?"],
              "2015": [act_south[0], demand_south[0], act_south[0]-demand_south[0], roles_s[0], transmission_south_out[0], transmission_south_in[0], transmission_south_out[0] - transmission_south_in[0], (((transmission_south_out[0]-transmission_south_in[0]) - (act_south[0] - demand_south[0]))), answers_s[0]],
              "2020": [act_south[1], demand_south[1], act_south[1]-demand_south[1], roles_s[1], transmission_south_out[1], transmission_south_in[1], transmission_south_out[1] - transmission_south_in[1], (((transmission_south_out[1]-transmission_south_in[1]) - (act_south[1] - demand_south[1]))), answers_s[1]],        
              "2025": [act_south[2], demand_south[2], act_south[2]-demand_south[2], roles_s[2], transmission_south_out[2], transmission_south_in[2], transmission_south_out[2] - transmission_south_in[2], (((transmission_south_out[2]-transmission_south_in[2]) - (act_south[2] - demand_south[2]))), answers_s[2]]}

values_s = pd.DataFrame(values_s)

print(values_s)

###################





mp.close_db()



####
####
####"""
#### Tarefas
####[x] 1. Região SE/CE (aprender a subdividir)
####    [x] Trocar country por subsystem
####[x] 2. Colocar 4 subsystems
####[x] 3. Conectar 2 subsystems (SE/CE e Sul) (ambos os sentidos)
####[x] 4. (Jon e Ric) Conectar todas as subsystems (respeitando geografia)
####[x] 5. Calibrar características das subsystems
####    [x] (Ric 1) Renomear tecnologias, evidenciando o nome de cada uma:
####        1.listar no inicio,  # "pch_NE_ppl"
####        2.copiar link para cada tecnologia 
####        3.ctrl+C e ctrl+V descrição de custos para cada tecnologia
####    [x] (?) Acrescentar ifs em cada modulo, para customizar dados de entrada por subsystem
####[] 6. Revisar unidades no programa (USD, MW e MWa) - 
####    1. Conferir nos exemplos Westros e Austria (e no GAMS?)
####    2. Conferir as unidades na planilha (ou no artigo mesmo)
####[x] 7. (Jon 1) Acrescentar tecnologia household para depois virar serviço energético
####[x] 8. (Ric 2) Trocar termos para inglês
####Obs: os dados inseridos devem contemplar todas as regioes.
####"""
