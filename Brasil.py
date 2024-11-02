import pandas as pd
import ixmp
import message_ix
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
from tkinter import messagebox
import tkinter as tk

from message_ix.utils import make_df

import inicio
import link
import descreve
import limites
import saidas


mp = ixmp.Platform()


scenario = message_ix.Scenario(mp, model="Brazil Electrified", scenario="baseline", version="new")


scenario, history, model_horizon, country, nodes    = inicio.definicoes (pd,scenario)

for local in nodes:
    scenario                                            = inicio.demanda    (pd,scenario,model_horizon,local)
    vintage_years, act_years,base_input, base_output    = link.base         (make_df,scenario,local)
    scenario, grid_efficiency                           = link.tecnologias  (scenario,base_input, base_output,local)
    scenario, capacity_factor               = descreve.fator_capacidade     (make_df,scenario,local,vintage_years, act_years)
    scenario                                = descreve.vida_util            (make_df,scenario,local,model_horizon)
    scenario                                = descreve.expande_tecnologias  (make_df,scenario,local,model_horizon)
    scenario                                = descreve.historico_geracao    (make_df,scenario,grid_efficiency,local,history,capacity_factor)
    scenario                                = descreve.custo_investimento   (make_df,scenario,local,model_horizon)
    scenario                                = descreve.custo_fixo           (make_df,scenario,local,vintage_years, act_years)
    scenario                                = descreve.custo_variavel       (make_df,scenario,local,vintage_years, act_years)
    scenario                                = limites.expansao_up           (make_df,scenario,local)

scenario = link.transmissao_S_SE(make_df,scenario)
scenario = link.transmissao_SE_S(make_df,scenario)
scenario = link.transmissao_SE_NE(make_df,scenario)
scenario = link.transmissao_NE_SE(make_df,scenario)
scenario = link.transmissao_N_NE(make_df,scenario)
scenario = link.transmissao_NE_N(make_df,scenario)
scenario = link.transmissao_N_SE(make_df,scenario)
scenario = link.transmissao_SE_N(make_df,scenario)

scenario.solve()


#saidas.gera_excel(pd,scenario)

tk.messagebox.showinfo("Notification", "The code has been successfully run!")


mp.close_db()



"""
# Tarefas
[x] 1. Região SE/CE (aprender a subdividir)
    [x] Trocar country por subsystem
[x] 2. Colocar 4 subsystems
[x] 3. Conectar 2 subsystems (SE/CE e Sul) (ambos os sentidos)
[] 4. (Jon 2) Conectar todas as subsystems (respeitando geografia)
[] 5. Calibrar características das subsystems
    [x] (Ric 1) Renomear tecnologias, evidenciando o nome de cada uma:
        1.listar no inicio,  # "pch_NE_ppl"
        2.copiar link para cada tecnologia 
        3.ctrl+C e ctrl+V descrição de custos para cada tecnologia
    [] (?) Acrescentar ifs em cada modulo, para customizar dados de entrada por subsystem
[] 6. Revisar unidades no programa (USD, MW e MWa) - 
    1. Conferir nos exemplos Westros e Austria (e no GAMS?)
    2. Conferir as unidades na planilha (ou no artigo mesmo)
[x] 7. (Jon 1) Acrescentar tecnologia household para depois virar serviço energético
[] 8. (Ric 2) Trocar termos para inglês
Obs: os dados inseridos devem contemplar todas as regioes.
"""
