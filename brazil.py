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


outputs.generate_excel(pd,scenario)

tk.messagebox.showinfo("Notification", "The code has been successfully run!")


mp.close_db()



"""
# Tarefas
[x] 1. Região SE/CE (aprender a subdividir)
    [x] Trocar country por subsystem
[x] 2. Colocar 4 subsystems
[x] 3. Conectar 2 subsystems (SE/CE e Sul) (ambos os sentidos)
[x] 4. (Jon e Ric) Conectar todas as subsystems (respeitando geografia)
[x] 5. Calibrar características das subsystems
    [x] (Ric 1) Renomear tecnologias, evidenciando o nome de cada uma:
        1.listar no inicio,  # "pch_NE_ppl"
        2.copiar link para cada tecnologia 
        3.ctrl+C e ctrl+V descrição de custos para cada tecnologia
    [x] (?) Acrescentar ifs em cada modulo, para customizar dados de entrada por subsystem
[] 6. Revisar unidades no programa (USD, MW e MWa) - 
    1. Conferir nos exemplos Westros e Austria (e no GAMS?)
    2. Conferir as unidades na planilha (ou no artigo mesmo)
[x] 7. (Jon 1) Acrescentar tecnologia household para depois virar serviço energético
[x] 8. (Ric 2) Trocar termos para inglês
Obs: os dados inseridos devem contemplar todas as regioes.
"""
