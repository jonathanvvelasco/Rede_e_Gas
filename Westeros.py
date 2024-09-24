import pandas as pd
import ixmp
import message_ix
from matplotlib.pyplot import *
from message_ix.utils import make_df


mp = ixmp.Platform()

scenario = message_ix.Scenario(
    mp, model="Westeros Electrified", scenario="baseline", version="new"
)

history = [690]
model_horizon = [700, 710, 720]
scenario.add_horizon(year=history + model_horizon, firstmodelyear=model_horizon[0])

country = "Westeros"
scenario.add_spatial_sets({"country": country})

scenario.add_set("commodity", ["electricity", "light"])
scenario.add_set("level", ["secondary", "final", "useful"])
scenario.add_set("technology", ["coal_ppl", "wind_ppl", "grid", "bulb"])
scenario.add_set("mode", "standard")

gdp_profile = pd.Series([1.0, 1.5, 1.9], index=pd.Index(model_horizon, name="Time"))
gdp_profile.plot(title="GDP profile")

demand_per_year = 40 * 12 * 1000 / 8760
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

coal_out = base_output.assign(
    technology="coal_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)
scenario.add_par("output", coal_out)

wind_out = base_output.assign(
    technology="wind_ppl",
    commodity="electricity",
    level="secondary",
    value=1.0,
    unit="GWa",
)
scenario.add_par("output", wind_out)

capacity_factor = {
    "coal_ppl": 1,
    "wind_ppl": 0.36,
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
    "coal_ppl": 20,
    "wind_ppl": 20,
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
    "coal_ppl",
    "wind_ppl",
]

for tec in growth_technologies:
    df = make_df(
        "growth_activity_up",
        node_loc=country,
        year_act=model_horizon,
        time="year",
        unit="-",
        technology=tec,
        value=0.1,
    )
    scenario.add_par("growth_activity_up", df)

#####################################################
#####################################################
#Parte que precisa ser removida

historic_demand = 0.5 * demand_per_year
historic_generation = historic_demand / grid_efficiency
coal_fraction = 0.5

old_activity = {
    "coal_ppl": coal_fraction * historic_generation,
    "wind_ppl": (1 - coal_fraction) * historic_generation,
}

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
#####################################################
#####################################################

mp.add_unit("USD/kW")


costs = {
    "coal_ppl": 500,
    "wind_ppl": 1500,
    "bulb": 5,
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



costs = {
    "coal_ppl": 30,
    "wind_ppl": 10,
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
    "coal_ppl": 30,
    "grid": 50,
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

scenario.commit(comment="basic model of Westeros electrification")

log.info(f"version number after commit(): {scenario.version}")

scenario.set_as_default()
scenario.solve()
scenario.var("OBJ")["lvl"]



from message_ix.report import Reporter

rep = Reporter.from_scenario(scenario)


from message_ix.util.tutorial import prepare_plots

prepare_plots(rep)

rep.set_filters(t=["coal_ppl", "wind_ppl"])
rep.get("plot activity")
rep.get("plot capacity")
rep.get("plot new capacity")
rep.set_filters(c=["light"])
rep.get("plot prices")
a = pd.DataFrame(scenario.var("ACT"))
a.to_excel("Atividade.xlsx")
b = pd.DataFrame(scenario.var("CAP"))
b.to_excel("Capacidade.xlsx")
c = pd.DataFrame(scenario.var("CAP_NEW"))
c.to_excel("Nova Capacidade das Instalações.xlsx")


mp.close_db()
