import pandas as pd
import ixmp
import message_ix
from matplotlib.pyplot import *
import matplotlib.pyplot as plt

from message_ix.utils import make_df


mp = ixmp.Platform()

scenario = message_ix.Scenario(
    mp, model="Brazil Electrified", scenario="baseline", version="new"
)

# ============================================ Definicoes ==============================================================

# Define ano historico e anos de simulacao
history = [2010]
model_horizon = [2015, 2020, 2025]
scenario.add_horizon(year=history + model_horizon, firstmodelyear=model_horizon[0])

# Define pais e subdivisoes
country = "Brazil"
# regioes = ["Norte, Nordeste"...] # A gente pode olhar o codigo do Fernando para inspiracao
scenario.add_spatial_sets({"country": country})
# scenario.add_spatial_sets({"province": regioes})

# Tarefas
# 1. Região SE/CE (aprender a subdividir)
# 2. Colocar 4 regiões
# 3. Conectar 2 regiões (SE/CE e Sul) (ambos os sentidos)
# 4. Conectar todas as rgiões (respeitando geografia)
# 5. Calibrar características das regiões


#Definindo regiões

scenario.set('map_spatial_hierarchy')

nodes = ['South', 'Northeast']
space_level = 'province'
scenario.add_set('lvl_spatial', space_level)
for node in nodes:
    scenario.add_set('node', node)
    scenario.add_set('map_spatial_hierarchy', [space_level, node, country])

scenario.set('map_spatial_hierarchy')


# Define tecnologias

scenario.add_set("commodity", ["electricity", "light"])
scenario.add_set("level", ["secondary", "final", "useful"])
scenario.add_set("technology", ["oil_ppl", "pch_ppl","nuclear_g_ppl", "biogas_ppl", "solar_fotovoltaic_ppl", "solar_csp_ppl","onshore_wind_ppl", "offshore_wind_ppl","biomass_retrofit_ppl", "biomass_greenfield_ppl","GN_open_cycle_ppl", "GN_combined_cycle_ppl","national_coal_ppl", "imported_coal_ppl","large_hydroelectric_ppl", "medium_hydroelectric_ppl","grid", "bulb"])
scenario.add_set("mode", 'standard')
scenario.set("mode")
#=============================================================================================================================


# ============================================ Input de Demanda ==============================================================

#Insere valores de demanda em MWmédios
demanda = pd.Series([77883, 100861, 119496], index=pd.Index(model_horizon, name="Time"))

# Cria uso final da demanda
light_demand = pd.DataFrame(
    {
        "node": country,
        "commodity": "light",
        "level": "useful",
        "year": model_horizon,
        "time": "year",
        "value": (demanda).round(),
        "unit": "MWa",
    }
)
scenario.add_par("demand", light_demand)
#=============================================================================================================================

# Le anos de construcao e anos de producao
year_df = scenario.vintage_and_active_years()
vintage_years, act_years = year_df["year_vtg"], year_df["year_act"]


# ======================================= Links Input e Output ===============================================================
# Cria classe base para Input e Output
base = dict(
    node_loc=country,
    year_vtg=vintage_years,
    year_act=act_years,
    mode='standard',
    time="year",
    unit="-",
)

base_input = make_df("input", **base, node_origin=country, time_origin="year")

base_output = make_df("output", **base, node_dest=country, time_dest="year")


bulb_out = base_output.assign(
    technology="bulb", commodity="light", level="useful", value=1.0
)
scenario.add_par("output", bulb_out)

bulb_in = base_input.assign(
    technology="bulb", commodity="electricity", level="final", value=1.0
)
scenario.add_par("input", bulb_in)

scenario.idx_names("input")

grid_efficiency = 1
grid_out = base_output.assign(
    technology="grid",
    commodity="electricity",
    level="final",
    value=grid_efficiency,
)
scenario.add_par("output", grid_out)

grid_in = base_input.assign(
    technology="grid", commodity="electricity", level="secondary", value=1.0
)
scenario.add_par("input", grid_in)

oil_out = base_output.assign(
    technology="oil_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)
scenario.add_par("output", oil_out)

pch_out = base_output.assign(
    technology="pch_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)
scenario.add_par("output", pch_out)

nuclear_g_out = base_output.assign(
    technology="nuclear_g_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)
scenario.add_par("output", nuclear_g_out)

biogas_out = base_output.assign(
    technology="biogas_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)
scenario.add_par("output", biogas_out)

solar_fotovoltaic_out = base_output.assign(
    technology="solar_fotovoltaic_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)
scenario.add_par("output", solar_fotovoltaic_out)

solar_csp_out = base_output.assign(
    technology="solar_csp_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)
scenario.add_par("output", solar_csp_out)

onshore_wind_out = base_output.assign(
    technology="onshore_wind_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)
scenario.add_par("output", onshore_wind_out)

offshore_wind_out = base_output.assign(
    technology="offshore_wind_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)
scenario.add_par("output", offshore_wind_out)

biomass_retrofit_out = base_output.assign(
    technology="biomass_retrofit_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)
scenario.add_par("output", biomass_retrofit_out)

biomass_greenfield_out = base_output.assign(
    technology="biomass_greenfield_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)
scenario.add_par("output", biomass_greenfield_out)

GN_open_cycle_out = base_output.assign(
    technology="GN_open_cycle_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)
scenario.add_par("output", GN_open_cycle_out)

GN_combined_cycle_out = base_output.assign(
    technology="GN_combined_cycle_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)
scenario.add_par("output", GN_combined_cycle_out)


large_hydroelectric_out = base_output.assign(
    technology="large_hydroelectric_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)
scenario.add_par("output", large_hydroelectric_out)

medium_hydroelectric_out = base_output.assign(
    technology="medium_hydroelectric_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)
scenario.add_par("output", medium_hydroelectric_out)

national_coal_out = base_output.assign(
    technology="national_coal_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)
scenario.add_par("output", national_coal_out)

imported_coal_out = base_output.assign(
    technology="imported_coal_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)
scenario.add_par("output", imported_coal_out)

#=====South=====#

base_input_n1 = {
    'node_loc': 'South',
    'node_origin': 'South',
    'commodity': 'electricity',
    'year_vtg': vintage_years,
    'year_act': act_years,
    'mode': 's-to-s',
    'time': 'year',
    'time_origin': 'year',
    'unit': '-',
}

base_output_n1 = {
    'node_loc': 'South',
    'node_dest': 'South',
    'commodity': 'electricity',
    'year_vtg': vintage_years,
    'year_act': act_years,
    'mode': 's-to-s',
    'time': 'year',
    'time_dest': 'year',
    'unit': '-',
}



capacity_factor = {
    "oil_ppl": 0.2,
    "pch_ppl": 0.5,
    "nuclear_g_ppl":0.85,
    "biogas_ppl":0.5,
    "solar_fotovoltaic_ppl":0.4,
    "solar_csp_ppl":0.2,
    "onshore_wind_ppl":0.3,
    "offshore_wind_ppl":0.3,
    "biomass_retrofit_ppl":0.67,
    "biomass_greenfield_ppl":0.67,
    "GN_open_cycle_ppl":0.4,
    "GN_combined_cycle_ppl":0.6,
    "national_coal_ppl":0.4,
    "imported_coal_ppl":0.5,
    "large_hydroelectric_ppl":0.5,
    "medium_hydroelectric_ppl":0.55,
    "bulb": 1,
}

for tec, val in capacity_factor.items():
    df = make_df(
        "capacity_factor",
        node_loc=country,
        year_vtg=vintage_years,
        year_act=act_years,
        time="year",
        unit="-",
        technology=tec,
        value=val,
    )
    scenario.add_par("capacity_factor", df)

    lifetime = {
    "oil_ppl": 20,
    "pch_ppl": 20,
    "nuclear_g_ppl":20,
    "biogas_ppl":20,
    "solar_fotovoltaic_ppl":20,
    "solar_csp_ppl":20,
    "onshore_wind_ppl":20,
    "offshore_wind_ppl":20,
    "biomass_retrofit_ppl":40,
    "biomass_greenfield_ppl":20,
    "GN_open_cycle_ppl":20,
    "GN_combined_cycle_ppl":20,
    "national_coal_ppl":35,
    "imported_coal_ppl":35,
    "large_hydroelectric_ppl":50,
    "medium_hydroelectric_ppl":50,
    "bulb": 1,
}

for tec, val in lifetime.items():
    df = make_df(
        "technical_lifetime",
        node_loc=country,
        year_vtg=model_horizon,
        unit="y",
        technology=tec,
        value=val,
    )
    scenario.add_par("technical_lifetime", df)


growth_technologies = [
    "pch_ppl",
    "nuclear_g_ppl",
    "biogas_ppl",
    "solar_fotovoltaic_ppl",
    "solar_csp_ppl",
    "onshore_wind_ppl",
    "offshore_wind_ppl",
    "biomass_retrofit_ppl",
    "biomass_greenfield_ppl",
    "GN_open_cycle_ppl",
    "GN_combined_cycle_ppl",
    "national_coal_ppl",
    "imported_coal_ppl",
    "large_hydroelectric_ppl",
    "medium_hydroelectric_ppl",
]

for tec in growth_technologies:
    df = make_df(
        "growth_activity_up",
        node_loc=country,
        year_act=model_horizon,
        time="year",
        unit="-",
        technology=tec,
        value=1.0,
    )
    scenario.add_par("growth_activity_up", df)


historic_demand =  60194
historic_generation = historic_demand / grid_efficiency
large_hydroelectric_fraction = 0.73532
pch_fraction = 0.04153
national_coal_fraction = 0.01339
gn_fraction = 0.07709
biomass_fraction = 0.05899
wind_fraction = 0.03887
nuclear_fraction  = 0.02834
oil_fraction = 0.00645



old_activity = {
    "large_hydroelectric_ppl":(large_hydroelectric_fraction) * historic_generation,
    "oil_ppl": oil_fraction * historic_generation,
    "nuclear_g_ppl": nuclear_fraction*historic_generation,
    "national_coal_ppl": national_coal_fraction* historic_generation,
    "biomass_retrofit_ppl": biomass_fraction * historic_generation,
    "onshore_wind_ppl": wind_fraction* historic_generation,
    "GN_open_cycle_ppl": gn_fraction * historic_generation,
    "pch_ppl": pch_fraction * historic_generation,

}
nomes_energias = []
uso_energias = []


for i in old_activity.items():
    nomes_energias.append(i[0])
    uso_energias.append(i[1])


plt.pie(uso_energias, shadow = True, autopct = "%.2f%%", pctdistance=1.15, startangle = 0, textprops={'fontsize': 9})
plt.title("Proportions Usage")
plt.legend(nomes_energias, loc='upper right', bbox_to_anchor=(1.68,0.85))
plt.gcf().set_size_inches(10, 5)
plt.savefig('6.png', dpi=200)
plt.figure().clear()


capacity = {"biomass_retrofit_ppl": 20,
       }

base_capacity = {
    'node_loc': country,
    'year_vtg': [2015, 2020, 2025],
    'unit': 'GW',
}

##cf = pd.Series(capacity_factor)
##act = pd.Series(activity)
#capacity = (act / 8760 / cf).dropna().to_dict()

for tec, val in capacity.items():
    df = make_df(base_capacity, technology=tec, value=val)
    scenario.add_par('bound_new_capacity_up', df)


for tec, val in old_activity.items():
    df = make_df(
        "historical_activity",
        node_loc=country,
        year_act=history,
        mode="standard",
        time="year",
        unit="GWa",
        technology=tec,
        value=val,
    )
    scenario.add_par("historical_activity", df)


for tec in old_activity:
    value = old_activity[tec] / (1 * 10 * capacity_factor[tec])
    df = make_df(
        "historical_new_capacity",
        node_loc=country,
        year_vtg=history,
        unit="GWa",
        technology=tec,
        value=value,
    )
    scenario.add_par("historical_new_capacity", df)


scenario.add_par("interestrate", model_horizon, value=0.05, unit="-")


mp.add_unit("USD/kW")

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
energias = []
custos =[]
for j in costs.items():
    if j[0] != 'bulb':
        energias.append(j[0])
        custos.append(j[1])

plt.pie(custos, shadow = True, startangle = 0, textprops={'fontsize': 9}, labels = custos)
plt.title("Investment Costs (USD/kW)")
plt.legend(energias, loc='upper right', bbox_to_anchor=(1.68,0.85))
plt.gcf().set_size_inches(10, 5)
plt.figure().clear()

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


#=====Northeast=====#

base_input_n1 = {
    'node_loc': 'Northeast',
    'node_origin': 'Northeast',
    'commodity': 'electricity',
    'year_vtg': vintage_years,
    'year_act': act_years,
    'mode': 'ne-to-ne',
    'time': 'year',
    'time_origin': 'year',
    'unit': '-',
}

base_output_n1 = {
    'node_loc': 'Northeast',
    'node_dest': 'Northeast',
    'commodity': 'electricity',
    'year_vtg': vintage_years,
    'year_act': act_years,
    'mode': 'ne-to-ne',
    'time': 'year',
    'time_dest': 'year',
    'unit': '-',
}


capacity_factor = {
    "oil_ppl": 0.1,
    "pch_ppl": 0.5,
    "nuclear_g_ppl":0.55,
    "biogas_ppl":0.5,
    "solar_fotovoltaic_ppl":0.2,
    "solar_csp_ppl":0.2,
    "onshore_wind_ppl":0.3,
    "offshore_wind_ppl":0.3,
    "biomass_retrofit_ppl":0.27,
    "biomass_greenfield_ppl":0.37,
    "GN_open_cycle_ppl":0.4,
    "GN_combined_cycle_ppl":0.6,
    "national_coal_ppl":0.4,
    "imported_coal_ppl":0.5,
    "large_hydroelectric_ppl":0.5,
    "medium_hydroelectric_ppl":0.55,
    "bulb": 1,
}

for tec, val in capacity_factor.items():
    df = make_df(
        "capacity_factor",
        node_loc=country,
        year_vtg=vintage_years,
        year_act=act_years,
        time="year",
        unit="-",
        technology=tec,
        value=val,
    )
    scenario.add_par("capacity_factor", df)

    lifetime = {
    "oil_ppl": 20,
    "pch_ppl": 20,
    "nuclear_g_ppl":20,
    "biogas_ppl":20,
    "solar_fotovoltaic_ppl":20,
    "solar_csp_ppl":20,
    "onshore_wind_ppl":20,
    "offshore_wind_ppl":20,
    "biomass_retrofit_ppl":40,
    "biomass_greenfield_ppl":20,
    "GN_open_cycle_ppl":20,
    "GN_combined_cycle_ppl":20,
    "national_coal_ppl":35,
    "imported_coal_ppl":35,
    "large_hydroelectric_ppl":50,
    "medium_hydroelectric_ppl":50,
    "bulb": 1,
}

for tec, val in lifetime.items():
    df = make_df(
        "technical_lifetime",
        node_loc=country,
        year_vtg=model_horizon,
        unit="y",
        technology=tec,
        value=val,
    )
    scenario.add_par("technical_lifetime", df)


growth_technologies = [
    "pch_ppl",
    "nuclear_g_ppl",
    "biogas_ppl",
    "solar_fotovoltaic_ppl",
    "solar_csp_ppl",
    "onshore_wind_ppl",
    "offshore_wind_ppl",
    "biomass_retrofit_ppl",
    "biomass_greenfield_ppl",
    "GN_open_cycle_ppl",
    "GN_combined_cycle_ppl",
    "national_coal_ppl",
    "imported_coal_ppl",
    "large_hydroelectric_ppl",
    "medium_hydroelectric_ppl",
]

for tec in growth_technologies:
    df = make_df(
        "growth_activity_up",
        node_loc=country,
        year_act=model_horizon,
        time="year",
        unit="-",
        technology=tec,
        value=1.0,
    )
    scenario.add_par("growth_activity_up", df)


historic_demand =  60194
historic_generation = historic_demand / grid_efficiency
large_hydroelectric_fraction = 0.73532
pch_fraction = 0.04153
national_coal_fraction = 0.01339
gn_fraction = 0.07709
biomass_fraction = 0.05899
wind_fraction = 0.03887
nuclear_fraction  = 0.02834
oil_fraction = 0.00645



old_activity = {
    "large_hydroelectric_ppl":(large_hydroelectric_fraction) * historic_generation,
    "oil_ppl": oil_fraction * historic_generation,
    "nuclear_g_ppl": nuclear_fraction*historic_generation,
    "national_coal_ppl": national_coal_fraction* historic_generation,
    "biomass_retrofit_ppl": biomass_fraction * historic_generation,
    "onshore_wind_ppl": wind_fraction* historic_generation,
    "GN_open_cycle_ppl": gn_fraction * historic_generation,
    "pch_ppl": pch_fraction * historic_generation,

}
nomes_energias = []
uso_energias = []


for i in old_activity.items():
    nomes_energias.append(i[0])
    uso_energias.append(i[1])


plt.pie(uso_energias, shadow = True, autopct = "%.2f%%", pctdistance=1.15, startangle = 0, textprops={'fontsize': 9})
plt.title("Proportions Usage")
plt.legend(nomes_energias, loc='upper right', bbox_to_anchor=(1.68,0.85))
plt.gcf().set_size_inches(10, 5)
plt.savefig('6.png', dpi=200)
plt.figure().clear()


capacity = {"biomass_retrofit_ppl": 20,
       }

base_capacity = {
    'node_loc': country,
    'year_vtg': [2015, 2020, 2025],
    'unit': 'GW',
}

##cf = pd.Series(capacity_factor)
##act = pd.Series(activity)
#capacity = (act / 8760 / cf).dropna().to_dict()

for tec, val in capacity.items():
    df = make_df(base_capacity, technology=tec, value=val)
    scenario.add_par('bound_new_capacity_up', df)


for tec, val in old_activity.items():
    df = make_df(
        "historical_activity",
        node_loc=country,
        year_act=history,
        mode="standard",
        time="year",
        unit="GWa",
        technology=tec,
        value=val,
    )
    scenario.add_par("historical_activity", df)


for tec in old_activity:
    value = old_activity[tec] / (1 * 10 * capacity_factor[tec])
    df = make_df(
        "historical_new_capacity",
        node_loc=country,
        year_vtg=history,
        unit="GWa",
        technology=tec,
        value=value,
    )
    scenario.add_par("historical_new_capacity", df)


scenario.add_par("interestrate", model_horizon, value=0.05, unit="-")


mp.add_unit("USD/kW")

costs = {
    "oil_ppl": 100,
    "pch_ppl": 2030,
    "nuclear_g_ppl":2200,
    "biogas_ppl":2400,
    "solar_fotovoltaic_ppl":5900,
    "solar_csp_ppl":4800,
    "onshore_wind_ppl":2500,
    "offshore_wind_ppl":3500,
    "biomass_retrofit_ppl":1500,
    "biomass_greenfield_ppl":1100,
    "GN_open_cycle_ppl":1850,
    "GN_combined_cycle_ppl":1200,
    "national_coal_ppl":1100,
    "imported_coal_ppl":2600,
    "large_hydroelectric_ppl":1100,
    "medium_hydroelectric_ppl":1100,
    "bulb": 1,
    
}
energias = []
custos =[]
for j in costs.items():
    if j[0] != 'bulb':
        energias.append(j[0])
        custos.append(j[1])

plt.pie(custos, shadow = True, startangle = 0, textprops={'fontsize': 9}, labels = custos)
plt.title("Investment Costs (USD/kW)")
plt.legend(energias, loc='upper right', bbox_to_anchor=(1.68,0.85))
plt.gcf().set_size_inches(10, 5)
plt.figure().clear()

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

costs = {
    "oil_ppl": 40,
    "pch_ppl": 29,
    "nuclear_g_ppl":92,
    "biogas_ppl":169,
    "solar_fotovoltaic_ppl":12,
    "solar_csp_ppl":58,
    "onshore_wind_ppl":31,
    "offshore_wind_ppl":87,
    "biomass_retrofit_ppl":10,
    "biomass_greenfield_ppl":65,
    "GN_open_cycle_ppl":52,
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


b = pd.DataFrame(scenario.var("CAP"))
b.to_excel("Capacidade.xlsx")
c = pd.DataFrame(scenario.var("CAP_NEW"))
c.to_excel("Nova Capacidade das Instalações.xlsx")
d = pd.DataFrame(scenario.var("ACT"))
d.to_excel("Atividade.xlsx")





mp.close_db()

