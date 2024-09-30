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

history = [2000]
model_horizon = [2013, 2018, 2023]
scenario.add_horizon(year=history + model_horizon, firstmodelyear=model_horizon[0])

country = "Brazil"
scenario.add_spatial_sets({"country": country})

scenario.add_set("commodity", ["electricity", "light"])
scenario.add_set("level", ["secondary", "final", "useful"])
scenario.add_set("technology", ["large_hydroelectric_ppl", "medium_hydroelectric_ppl","grid", "bulb"])
scenario.add_set("mode", "standard")

gdp_profile = pd.Series([0.71, 1.59, 3.71], index=pd.Index(model_horizon, name="Time"))
gdp_profile.plot(title="GDP Growth")
savefig("1.png", dpi=500)

demand_per_year = 67 * 12 * 7059 / 8760
light_demand = pd.DataFrame(
    {
        "node": country,
        "commodity": "light",
        "level": "useful",
        "year": model_horizon,
        "time": "year",
        "value": (demand_per_year * gdp_profile).round(),
        "unit": "GWa",
    }
)

scenario.add_par("demand", light_demand)

year_df = scenario.vintage_and_active_years()
vintage_years, act_years = year_df["year_vtg"], year_df["year_act"]

base = dict(
    node_loc=country,
    year_vtg=vintage_years,
    year_act=act_years,
    mode="standard",
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



capacity_factor = {
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


historic_demand =  0.7* demand_per_year
historic_generation = historic_demand / grid_efficiency
medium_hydroelectric_fraction = 0.1
large_hydroelectric_fraction  = 0.2



old_activity = {
    "medium_hydroelectric_ppl":medium_hydroelectric_fraction * historic_generation,
    "large_hydroelectric_ppl":large_hydroelectric_fraction * historic_generation,

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




costs = {

   
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

