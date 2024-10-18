import pandas as pd
import ixmp
import message_ix
from matplotlib.pyplot import *
import matplotlib.pyplot as plt

from message_ix.utils import make_df

import inicio


mp = ixmp.Platform()

scenario = message_ix.Scenario(mp, model="Brazil Electrified", scenario="baseline", version="new")

scenario = inicio.definicoes(pd,scenario)

# Tarefas
# 1. Região SE/CE (aprender a subdividir)
# 2. Colocar 4 regiões
# 3. Conectar 2 regiões (SE/CE e Sul) (ambos os sentidos)
# 4. Conectar todas as rgiões (respeitando geografia)
# 5. Calibrar características das regiões




mp.close_db()

