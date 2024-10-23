import pandas as pd
import ixmp
import message_ix
from matplotlib.pyplot import *
import matplotlib.pyplot as plt

from message_ix.utils import make_df

import inicio
import link
import descreve
import limites
import saidas


mp = ixmp.Platform()


scenario = message_ix.Scenario(mp, model="Brazil Electrified", scenario="baseline", version="new")


scenario, history, model_horizon, country, nodes    = inicio.definicoes (pd,scenario)
vintage_years, act_years,base_input, base_output    = link.base         (make_df,scenario,country)
scenario, grid_efficiency                           = link.tecnologias  (scenario,base_input, base_output)
scenario, capacity_factor               = descreve.fator_capacidade     (make_df,scenario,country,vintage_years, act_years)
scenario                                = descreve.vida_util            (make_df,scenario,country,model_horizon)
scenario                                = descreve.expande_tecnologias  (make_df,scenario,country,model_horizon)
scenario                                = descreve.historico_geracao    (make_df,scenario,grid_efficiency,country,history,capacity_factor)
scenario                                = descreve.custo_investimento   (make_df,scenario,country,model_horizon)
scenario                                = descreve.custo_fixo           (make_df,scenario,country,vintage_years, act_years)
scenario                                = descreve.custo_variavel       (make_df,scenario,country,vintage_years, act_years)
scenario                                = limites.expansao_up           (make_df,scenario,country)


scenario.solve()


#saidas.gera_excel(pd,scenario)


mp.close_db()

