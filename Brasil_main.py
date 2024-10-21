import pandas as pd
import ixmp
import message_ix
from matplotlib.pyplot import *
import matplotlib.pyplot as plt

from message_ix.utils import make_df

import inicio
import link


mp = ixmp.Platform()

scenario = message_ix.Scenario(mp, model="Brazil Electrified", scenario="baseline", version="new")
country = "Brazil"

scenario, history, model_horizon    = inicio.definicoes(pd,scenario)
vintage_years, act_years,base_input, base_output = link.base(make_df,scenario,"Brazil")
scenario, grid_efficiency    = link.tecnologias(scenario,base_input, base_output)

# Tarefas
# 1. Região SE/CE (aprender a subdividir)
# 2. Colocar 4 regiões
# 3. Conectar 2 regiões (SE/CE e Sul) (ambos os sentidos)
# 4. Conectar todas as rgiões (respeitando geografia)
# 5. Calibrar características das regiões




mp.close_db()

