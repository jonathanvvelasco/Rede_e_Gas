import itertools
import pandas as pd
import dask_expr as dx
from matplotlib.pyplot import *

import matplotlib.pyplot as plt
plt.style.use('ggplot')

import ixmp as ix
import message_ix

from message_ix.util import make_df

mp = ix.Platform()
model = "Brazilian energy model"
scen = "baseline"
annot = "developing a stylized energy system model for illustration and testing" 

scenario = message_ix.Scenario(mp, model, scen, version='new', annotation=annot)

horizon = range(2008, 2024, 5)
scenario.add_horizon(year=horizon)
country = 'Brazil'
scenario.add_spatial_sets({'country': country})

scenario.add_set("commodity", ["electricity", "light", "other_electricity"])
scenario.add_set("level", ["secondary", "final", "useful"])
scenario.add_set("mode", "standard")

scenario.add_par("interestrate", horizon, value=0.05, unit='-')

gdp = pd.Series([1., 1.59, 3.71, 3.24], index=horizon)
beta = 0.7
demand = gdp ** beta
gdp.plot(title="GDP Growth")

#saving the graph
savefig("1.png", dpi=500)

plants = [
    "national_coal_ppl",
    "imported_coal_ppl",
    "GN_open_cycle_ppl",
    "GN_combined_cycle_ppl",
    "nuclear_g_ppl",
    "biomass_retrofit_ppl",
    "biomass_greenfield_ppl",
    "biogas_ppl",
    "onshore_wind_ppl",
    "offshore_wind_ppl",
    "solar_fotovoltaic_ppl",
    "solar_csp_ppl",
    "large_hydroelectric_ppl",
    "medium_hydroelectric_ppl", 
]
secondary_energy_techs = plants

final_energy_techs = ['electricity_grid']

lights = [
    "bulb", 
]
useful_energy_techs = lights
technologies = secondary_energy_techs + final_energy_techs + useful_energy_techs
scenario.add_set("technology", technologies)
demand_per_year = 55209. / 8760 
elec_demand = pd.DataFrame({
        'node': country,
        'commodity': 'other_electricity',
        'level': 'useful',
        'year': horizon,
        'time': 'year',
        'value': demand_per_year * demand,
        'unit': 'GWa',
    })
scenario.add_par("demand", elec_demand)

demand_per_year = 6134. / 8760
light_demand = pd.DataFrame({
        'node': country,
        'commodity': 'light',
        'level': 'useful',
        'year': horizon,
        'time': 'year',
        'value': demand_per_year * demand,
        'unit': 'GWa',
    })
scenario.add_par("demand", light_demand)

year_df = scenario.vintage_and_active_years()
vintage_years, act_years = year_df['year_vtg'], year_df['year_act']
base_input = {
    'node_loc': country,
    'year_vtg': vintage_years,
    'year_act': act_years,
    'mode': 'standard',
    'node_origin': country,
    'commodity': 'electricity',
    'time': 'year',
    'time_origin': 'year',
}

grid = pd.DataFrame(dict(
        technology = 'electricity_grid',
        level = 'secondary',
        value = 1.0,
        unit = '-',
        **base_input
        ))
scenario.add_par("input", grid)


bulb = pd.DataFrame(dict(
        technology = 'bulb',
        level = 'final',
        value = 1.0,
        unit = '-',
        **base_input
        ))
scenario.add_par("input", bulb)


##app = pd.DataFrame(dict(
##        technology = 'appliances',
##        level = 'final',
##        value = 1.0,
##        unit = '-',
##        **base_input
##        ))
##scenario.add_par("input", app)
base_output = {
    'node_loc': country,
    'year_vtg': vintage_years,
    'year_act': act_years,
    'mode': 'standard',
    'node_dest': country,
    'time': 'year',
    'time_dest': 'year', 
    'unit': '-',
}

##imports = make_df(base_output, technology='import', commodity='electricity', 
##                  level='secondary', value=1.)
##scenario.add_par('output', imports)

grid = make_df(base_output, technology='electricity_grid', commodity='electricity', 
               level='final', value=0.873)
scenario.add_par('output', grid)

bulb = make_df(base_output, technology='bulb', commodity='light', 
               level='useful', value=1.)
scenario.add_par('output', bulb)


##app = make_df(base_output, technology='appliances', commodity='other_electricity', 
##              level='useful', value=1.)
##scenario.add_par('output', app)

national_coal = make_df(base_output, technology='national_coal_ppl', commodity='electricity', 
               level='secondary', value=1.)
scenario.add_par('output', national_coal)

imported_coal = make_df(base_output, technology='imported_coal_ppl', commodity='electricity', 
              level='secondary', value=1.)
scenario.add_par('output', imported_coal)

GN_open_cycle = make_df(base_output, technology='GN_open_cycle_ppl', commodity='electricity', 
              level='secondary', value=1.)
scenario.add_par('output', GN_open_cycle)

GN_combined_cycle = make_df(base_output, technology='GN_combined_cycle_ppl', commodity='electricity', 
              level='secondary', value=1.)
scenario.add_par('output', GN_combined_cycle)

nuclear_g = make_df(base_output, technology='nuclear_g_ppl', commodity='electricity', 
                level='secondary', value=1.)
scenario.add_par('output', nuclear_g)

biomass_retrofit = make_df(base_output, technology='biomass_retrofit_ppl', commodity='electricity', 
               level='secondary', value=1.)
scenario.add_par('output', biomass_retrofit)

biomass_greenfield = make_df(base_output, technology='biomass_greenfield_ppl', commodity='electricity', 
                   level='final', value=1.)
scenario.add_par('output', biomass_greenfield)

biogas = make_df(base_output, technology='biogas_ppl', commodity='electricity', 
                   level='final', value=1.)
scenario.add_par('output', biogas)

onshore_wind = make_df(base_output, technology='onshore_wind_ppl', commodity='electricity', 
                   level='final', value=1.)
scenario.add_par('output', onshore_wind)

offshore_wind = make_df(base_output, technology='offshore_wind_ppl', commodity='electricity', 
                   level='final', value=1.)
scenario.add_par('output', offshore_wind)

solar_fotovoltaic = make_df(base_output, technology='solar_fotovoltaic_ppl', commodity='electricity', 
                   level='final', value=1.)
scenario.add_par('output', solar_fotovoltaic)

solar_csp = make_df(base_output, technology='solar_csp_ppl', commodity='electricity', 
                   level='final', value=1.)
scenario.add_par('output', solar_csp)

large_hydroelectric = make_df(base_output, technology='large_hydroelectric_ppl', commodity='electricity', 
                   level='final', value=1.)
scenario.add_par('output', large_hydroelectric)

medium_hydroelectric = make_df(base_output, technology='medium_hydroelectric_ppl', commodity='electricity', 
                   level='final', value=1.)
scenario.add_par('output', medium_hydroelectric)
base_technical_lifetime = {
    'node_loc': country,
    'year_vtg': horizon,
    'unit': 'y',
}

lifetimes = {
    "national_coal_ppl":35,
    "imported_coal_ppl":35,
    "GN_open_cycle_ppl":20,
    "GN_combined_cycle_ppl":20,
    "nuclear_g_ppl":20,
    "biomass_retrofit_ppl":40,
    "biomass_greenfield_ppl":20,
    "biogas_ppl":20,
    "onshore_wind_ppl":20,
    "offshore_wind_ppl":20,
    "solar_fotovoltaic_ppl":20,
    "solar_csp_ppl":20,
    "large_hydroelectric_ppl":50,
    "medium_hydroelectric_ppl":50,
    "bulb": 1,
}

for tec, val in lifetimes.items():
    df = make_df(base_technical_lifetime, technology=tec, value=val)
    scenario.add_par('technical_lifetime', df)
base_capacity_factor = {
    'node_loc': country,
    'year_vtg': vintage_years,
    'year_act': act_years,
    'time': 'year',
    'unit': '-',
}

capacity_factor = {
    "national_coal_ppl":0.4,
    "imported_coal_ppl":0.5,
    "GN_open_cycle_ppl":0.4,
    "GN_combined_cycle_ppl":0.6,
    "nuclear_g_ppl":0.85,
    "biomass_retrofit_ppl":0.67,
    "biomass_greenfield_ppl":0.67,
    "biogas_ppl":0.5,
    "onshore_wind_ppl":0.3,
    "offshore_wind_ppl":0.3,
    "solar_fotovoltaic_ppl":0.4,
    "solar_csp_ppl":0.2,
    "large_hydroelectric_ppl":0.5,
    "medium_hydroelectric_ppl":0.55,
    "bulb": 0.1, 
}

for tec, val in capacity_factor.items():
    df = make_df(base_capacity_factor, technology=tec, value=val)
    scenario.add_par('capacity_factor', df)

    base_inv_cost = {
    'node_loc': country,
    'year_vtg': horizon,
    'unit': 'USD/kW',
}

mp.add_unit('USD/kW')    

costs = {
    "national_coal_ppl":2100,
    "imported_coal_ppl":2100,
    "GN_open_cycle_ppl":2500,
    "GN_combined_cycle_ppl":3100,
    "nuclear_g_ppl":3500,
    "biomass_retrofit_ppl":1500,
    "biomass_greenfield_ppl":1900,
    "biogas_ppl":2400,
    "onshore_wind_ppl":2500,
    "offshore_wind_ppl":3500,
    "solar_fotovoltaic_ppl":3000,
    "solar_csp_ppl":3200,
    "large_hydroelectric_ppl":2700,
    "medium_hydroelectric_ppl":2100,
    "bulb": 5,
}

for tec, val in costs.items():
    df = make_df(base_inv_cost, technology=tec, value=val)
    scenario.add_par('inv_cost', df)
base_fix_cost = {
    'node_loc': country,
    'year_vtg': vintage_years,
    'year_act': act_years,
    'unit': 'USD/kWa',
}


energias = []
custos =[]
for j in costs.items():
    if j[0] != 'bulb':
        energias.append(j[0])
        custos.append(j[1])

#saving the graph
plt.pie(custos, shadow = True, startangle = 0, textprops={'fontsize': 9}, labels = custos)
plt.title("Investment Costs (USD/kW)")
plt.legend(energias, loc='upper right', bbox_to_anchor=(1.68,0.85))
plt.gcf().set_size_inches(10, 5)
plt.savefig('10.png', dpi=200)
plt.figure().clear()

mp.add_unit('USD/kWa')  



costs = {
    "national_coal_ppl":28,
    "imported_coal_ppl":28,
    "GN_open_cycle_ppl":12,
    "GN_combined_cycle_ppl":18,
    "nuclear_g_ppl":92,
    "biomass_retrofit_ppl":10,
    "biomass_greenfield_ppl":65,
    "biogas_ppl":169,
    "onshore_wind_ppl":31,
    "offshore_wind_ppl":87,
    "solar_fotovoltaic_ppl":12,
    "solar_csp_ppl":58,
    "large_hydroelectric_ppl":29,
    "medium_hydroelectric_ppl":29, 
}

for tec, val in costs.items():
    df = make_df(base_fix_cost, technology=tec, value=val)
    scenario.add_par('fix_cost', df)
base_var_cost = {
    'node_loc': country,
    'year_vtg': vintage_years,
    'year_act': act_years,
    'mode': 'standard',
    'time': 'year',
    'unit': 'USD/kWa',
}


costs = {
    "national_coal_ppl":4.7,
    "imported_coal_ppl":7.0,
    "GN_open_cycle_ppl":4.0,
    "GN_combined_cycle_ppl":2.3,
    "nuclear_g_ppl":0.6,
    "biomass_retrofit_ppl":14.0,
    "biomass_greenfield_ppl":7.0,
    'electricity_grid': 20.8,
}

for tec, val in costs.items():
    df = make_df(base_var_cost, technology=tec, value=val * 8760. / 1e3) # to convert it into USD/kWa
    scenario.add_par('var_cost', df)

    base_growth = {
    'node_loc': country,
    'year_act': horizon[1:],
    'value': 0.05,
    'time': 'year',
    'unit': '%',
}

growth_technologies = [
    "national_coal_ppl",
    "imported_coal_ppl",
    "GN_open_cycle_ppl",
    "GN_combined_cycle_ppl",
    "nuclear_g_ppl",
    "biomass_retrofit_ppl",
    "biomass_greenfield_ppl",
    "biogas_ppl",
    "onshore_wind_ppl",
    "offshore_wind_ppl",
    "solar_fotovoltaic_ppl",
    "solar_csp_ppl",
    "large_hydroelectric_ppl",
    "medium_hydroelectric_ppl",
    "bulb",
]

for tec in growth_technologies:
    df = make_df(base_growth, technology=tec)
    scenario.add_par('growth_activity_up', df)
base_initial = {
    'node_loc': country,
    'year_act': horizon[1:],
    'time': 'year',
    'unit': '%',
}

for tec in lights:
    df = make_df(base_initial, technology=tec, value=0.01 * light_demand['value'].loc[horizon[1:]])
    scenario.add_par('initial_activity_up', df)
base_activity = {
    'node_loc': country,
    'year_act': [2008],
    'mode': 'standard',
    'time': 'year',
    'unit': 'GWa',
}

activity = {
    "national_coal_ppl":10000,
    "imported_coal_ppl":8000,
    "GN_open_cycle_ppl":12000,
    "GN_combined_cycle_ppl":5000,
    "nuclear_g_ppl":4000,
    "biomass_retrofit_ppl":1000,
    "biomass_greenfield_ppl":1000,
    "biogas_ppl":70000,
    "onshore_wind_ppl":8500,
    "offshore_wind_ppl":2000,
    "solar_fotovoltaic_ppl":1000,
    "solar_csp_ppl":1000,
    "large_hydroelectric_ppl":34500,
    'medium_hydroelectric_ppl':19000,
    #'import': 2000,
    #'cfl': 0,
}


for tec, val in activity.items():
    df = make_df(base_activity, technology=tec, value=val / 8760.)
    scenario.add_par('bound_activity_up', df)
    scenario.add_par('bound_activity_lo', df)
base_capacity = {
    'node_loc': country,
    'year_vtg': [2008],
    'unit': 'GW',
}

cf = pd.Series(capacity_factor)
act = pd.Series(activity)
capacity = (act / 8760 / cf).dropna().to_dict()

for tec, val in capacity.items():
    df = make_df(base_capacity, technology=tec, value=val)
    scenario.add_par('bound_new_capacity_up', df)
base_activity = {
    'node_loc': country,
    'year_act': horizon[1:],
    'mode': 'standard',
    'time': 'year',
    'unit': 'GWa',
}

keep_activity = {
     "national_coal_ppl":20000,
    "imported_coal_ppl":8000,
    "GN_open_cycle_ppl":12000,
    "GN_combined_cycle_ppl":5000,
    "large_hydroelectric_ppl":30000,
    'medium_hydroelectric_ppl':21000,
    #'import': 2000,
}

for tec, val in keep_activity.items():
    df = make_df(base_activity, technology=tec, value=val / 8760.)
    scenario.add_par('bound_activity_up', df)


comment = 'initial commit for Brazil model'
scenario.commit(comment)
scenario.set_as_default()
scenario.solve()
scenario.var('OBJ')['lvl']

from message_ix.report import Reporter
from message_ix.util.tutorial import prepare_plots

rep = Reporter.from_scenario(scenario)
prepare_plots(rep)
rep.set_filters(t=plants)

#saving the graphs
rep.get("plot new capacity")
plt.savefig("2.png", dpi=200, bbox_inches = "tight")
rep.set_filters(t=lights)
rep.get("plot new capacity")
plt.savefig("3.png", dpi=200, bbox_inches = "tight")
rep.set_filters(t=plants)
rep.get("plot capacity")
plt.savefig("4.png", dpi=200, bbox_inches = "tight")
rep.set_filters(t=lights)
rep.get("plot capacity")
plt.savefig("5.png", dpi=200, bbox_inches = "tight")
rep.get("plot demand")
plt.savefig("6.png", dpi=200, bbox_inches = "tight")
rep.set_filters(t=plants)
rep.get("plot activity")
plt.savefig("7.png", dpi=200, bbox_inches = "tight")
rep.set_filters(t=lights)
rep.get("plot activity")
plt.savefig("8.png", dpi=200, bbox_inches = "tight")
rep.set_filters(c=["light", "other_electricity"])
a = rep.get("plot prices")
plt.savefig("9.png", dpi=200, bbox_inches = "tight")


#exporting the data to excel
b = pd.DataFrame(scenario.var("CAP"))
b.to_excel("Capacidade.xlsx")
c = pd.DataFrame(scenario.var("CAP_NEW"))
c.to_excel("Nova Capacidade das Instalações.xlsx")
d = pd.DataFrame(scenario.var("ACT"))
d.to_excel("Atividade.xlsx")



mp.close_db()

