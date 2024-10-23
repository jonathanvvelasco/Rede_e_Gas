import pandas as pd
import ixmp
import message_ix
from matplotlib.pyplot import *
import matplotlib.pyplot as plt

from message_ix.utils import make_df

import inicio
import link
import descreve


mp = ixmp.Platform()

#mp.add_unit("USD/kW")
scenario = message_ix.Scenario(mp, model="Brazil Electrified", scenario="baseline", version="new")


scenario, history, model_horizon, country, nodes    = inicio.definicoes(pd,scenario)
vintage_years, act_years,base_input, base_output    = link.base(make_df,scenario,country)
scenario, grid_efficiency                           = link.tecnologias(scenario,base_input, base_output)
scenario, capacity_factor           = descreve.fator_capacidade(make_df,scenario,country,vintage_years, act_years)
scenario                            = descreve.vida_util(make_df,scenario,country,model_horizon)
scenario                            = descreve.expansao_tecnologias(make_df,scenario,country,model_horizon)
scenario        = descreve.historico_geracao(make_df,scenario,grid_efficiency,country,history,capacity_factor)

#------------------- Limita capacidade de biomassa ---------------------

capacity = {"biomass_retrofit_ppl": 20,
       }

base_capacity = {
    'node_loc': country,
    'year_vtg': [2015, 2020, 2025],
    'unit': 'MW',
}

for tec, val in capacity.items():
    df = make_df(base_capacity, technology=tec, value=val)
    scenario.add_par('bound_new_capacity_up', df)



#------------------- Descreve Custo de Investimento ---------------------
costs = {
    "oil_ppl": 10000,
    "pch_ppl": 2600,
    "nuclear_g_ppl":3500,
    "biogas_ppl":2400,
    "solar_fotovoltaic_ppl":5900,
    "solar_csp_ppl":4800,
    "onshore_wind_ppl":2500,
    "offshore_wind_ppl":3500,
    "biomass_retrofit_ppl":1500,
    "biomass_greenfield_ppl":1900,
    "GN_open_cycle_ppl":850,
    "GN_combined_cycle_ppl":1200,
    "national_coal_ppl":2100,
    "imported_coal_ppl":2100,
    "large_hydroelectric_ppl":1800,
    "medium_hydroelectric_ppl":2100,
    "bulb": 1,
    
}

for tec, val in costs.items():
    df = make_df(
        "inv_cost",
        node_loc=country,
        year_vtg=model_horizon,
        unit="USD/kW",
        technology=tec,
        value=val,
    )
    scenario.add_par("inv_cost", df)


#------------------- Descreve Custo Fixo ---------------------
costs = {
    "oil_ppl": 20,
    "pch_ppl": 29,
    "nuclear_g_ppl":92,
    "biogas_ppl":169,
    "solar_fotovoltaic_ppl":12,
    "solar_csp_ppl":58,
    "onshore_wind_ppl":31,
    "offshore_wind_ppl":87,
    "biomass_retrofit_ppl":10,
    "biomass_greenfield_ppl":65,
    "GN_open_cycle_ppl":12,
    "GN_combined_cycle_ppl":18,
    "national_coal_ppl":28,
    "imported_coal_ppl":28,
    "large_hydroelectric_ppl":29,
    "medium_hydroelectric_ppl":29,
    "bulb": 1,
}

for tec, val in costs.items():
    df = make_df(
        "fix_cost",
        node_loc=country,
        year_vtg=vintage_years,
        year_act=act_years,
        unit="USD/kWa",
        technology=tec,
        value=val,
    )
    scenario.add_par("fix_cost", df)


#------------------- Descreve Custo Variavel ---------------------
#O&M + Fuel
costs = {
    "biogas_ppl": 4.0,
    "nuclear_g_ppl":5.7 + 16,
    "national_coal_ppl":4.7 + 36.62,
    "imported_coal_ppl":7.0 + 19.12,
    "GN_open_cycle_ppl":4.0 + 75.60,
    "GN_combined_cycle_ppl":2.3 + 61.60,
    "biomass_retrofit_ppl":14.0,
    "biomass_greenfield_ppl":7.0,
   
}

for tec, val in costs.items():
    df = make_df(
        "var_cost",
        node_loc=country,
        year_vtg=vintage_years,
        year_act=act_years,
        mode="standard",
        time="year",
        unit="USD/kWa",
        technology=tec,
        value=val,
    )
    scenario.add_par("var_cost", df)


from message_ix import log

log.info(f"version number before commit(): {scenario.version}")

scenario.commit(comment="basic model of Brazil electrification")

log.info(f"version number after commit(): {scenario.version}")

scenario.set_as_default()


scenario.solve()

scenario.var("OBJ")["lvl"]

from message_ix.report import Reporter

rep = Reporter.from_scenario(scenario)


from message_ix.util.tutorial import prepare_plots

prepare_plots(rep)

'''
b = pd.DataFrame(scenario.var("CAP"))
b.to_excel("Capacidade.xlsx")
c = pd.DataFrame(scenario.var("CAP_NEW"))
c.to_excel("Nova Capacidade das Instalações.xlsx")
d = pd.DataFrame(scenario.var("ACT"))
d.to_excel("Atividade.xlsx")
'''




mp.close_db()

