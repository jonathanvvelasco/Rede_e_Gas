import pandas as pd
import ixmp
import message_ix
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
from tkinter import messagebox
import tkinter as tk
from message_ix.report import Reporter
from message_ix.util.tutorial import prepare_plots
from message_ix.utils import make_df

import begin
import connect
import connect_gas
import describe_electric
import limits
import outputs


mp = ixmp.Platform()
mp.add_unit("mi USD/GW")
mp.add_unit("mi USD/GW-a")
mp.add_unit("mi USD/GWa")
mp.add_unit("MMm3/day")


scenario = message_ix.Scenario(mp, model="Brasil Electrified", scenario="baseline", version="new")


scenario, history, model_horizon, country, nodes    = begin.definitions (pd,scenario)

for local in nodes:

    # ======================================= Describe electric sector
    scenario                                            = begin.demand_eletric  (pd,scenario,model_horizon,local)
    vintage_years, act_years,base_input, base_output    = connect.base          (make_df,scenario,local)
    scenario, grid_efficiency                           = connect.technologies  (scenario,base_input, base_output,local)
    scenario, capacity_factor               = describe_electric.capacity__factor         (make_df,scenario,local,vintage_years, act_years)
    scenario                                = describe_electric.life_time                (make_df,scenario,local,model_horizon)
    scenario                                = describe_electric.growth__tecnologies      (make_df,scenario,local,model_horizon)
    scenario, historic_demand_N, historic_demand_NE, historic_demand_S, historic_demand_SW, historic_act_N, historic_act_NE, historic_act_S, historic_act_SW                                = describe_electric.historic__generation    (make_df,scenario,local,history)
    scenario                                = describe_electric.historic__expansion      (make_df,scenario,local,history)
    scenario                                = describe_electric.inv_costs                (make_df,scenario,local,model_horizon)
    scenario                                = describe_electric.fix_costs                (make_df,scenario,local,vintage_years, act_years)
    scenario                                = describe_electric.var_costs                (make_df,scenario,local,vintage_years, act_years)

    # ======================================= Describe gas value chain
    scenario                                = begin.demand_gas                  (pd,scenario,model_horizon,local)
    scenario                                = connect_gas.technologies          (scenario,base_input,base_output, local)

    # ======================================= Include explicit limits
    scenario                                = limits.expansion_up               (make_df,scenario,local)
    scenario                                = limits.activity_up                (make_df,scenario,local)

# ======== Include Transmission of Electricity
scenario = connect.transmission_S_SE(make_df,scenario)
scenario = connect.transmission_SE_S(make_df,scenario)
scenario = connect.transmission_SE_NE(make_df,scenario)
scenario = connect.transmission_NE_SE(make_df,scenario)
scenario = connect.transmission_N_NE(make_df,scenario)
scenario = connect.transmission_NE_N(make_df,scenario)
scenario = connect.transmission_N_SE(make_df,scenario)
scenario = connect.transmission_SE_N(make_df,scenario)

# ======== Include Transmission of Natural Gas


scenario.solve()
scenario.var("OBJ")["lvl"]


#outputs.generate_excel(pd,scenario)
#outputs.validation_table(pd, scenario, historic_demand_N, historic_demand_NE, historic_demand_S, historic_demand_SW, historic_act_N, historic_act_NE, historic_act_S, historic_act_SW, history, model_horizon)
# outputs.plots(scenario, Reporter, prepare_plots, plt)
outputs.sankey(scenario,Reporter)

#tk.messagebox.showinfo("Notification", "The code has been successfully run!")


mp.close_db()

