# Módulo Link (Input e Output)

def base(make_df,scenario,local):
    # Define base de Link de Input e Output
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # 1- Le anos de construcao e anos de producao
    year_df = scenario.vintage_and_active_years()
    vintage_years, act_years = year_df["year_vtg"], year_df["year_act"]
    # 2- Cria classe base para Input e Output
    base = dict(
        node_loc=local,
        year_vtg=vintage_years,
        year_act=act_years,
        mode="standard",
        time="year",
        unit="-",
    )
    base_input = make_df("input", **base, node_origin=local, time_origin="year")
    base_output = make_df("output", **base, node_dest=local, time_dest="year")

    return vintage_years, act_years,base_input, base_output



def tecnologias(scenario,base_input,base_output):
    # Define Link de Input e Output para Tecnologias
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # Tecnologia Lampada (Final -> Util)
    bulb_out    = base_output.assign(technology="bulb", commodity="light", level="useful", value=1.0)
    bulb_in     = base_input.assign(technology="bulb", commodity="electricity", level="final", value=1.0)
    scenario.add_par("output", bulb_out)
    scenario.add_par("input", bulb_in)
    scenario.idx_names("input")

    # Tecnologia Rede Eletrica (Secundaria -> Final)
    grid_efficiency = 1
    grid_out = base_output.assign(technology="grid", commodity="electricity", level="final", value=grid_efficiency)
    grid_in  = base_input.assign(technology="grid", commodity="electricity", level="secondary", value=1.0)
    scenario.add_par("output", grid_out)
    scenario.add_par("input", grid_in)

    # Geracao a Oleo ( ... -> Secundaria)
    oil_out = base_output.assign(
        technology="oil_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", oil_out)

    # Geracao PCH ( ... -> Secundaria)
    pch_out = base_output.assign(
        technology="pch_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", pch_out)

    # Geracao Nuclear ( ... -> Secundaria)
    nuclear_g_out = base_output.assign(
        technology="nuclear_g_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", nuclear_g_out)

    # Geracao Biogas ( ... -> Secundaria)
    biogas_out = base_output.assign(
        technology="biogas_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", biogas_out)

    # Geracao Solar Fotovoltaica ( ... -> Secundaria)
    solar_fotovoltaic_out = base_output.assign(
        technology="solar_fotovoltaic_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", solar_fotovoltaic_out)

    # Geracao Solar CSP ( ... -> Secundaria)
    solar_csp_out = base_output.assign(
        technology="solar_csp_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", solar_csp_out)

    # Geracao Eolica Onshore ( ... -> Secundaria)
    onshore_wind_out = base_output.assign(
        technology="onshore_wind_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", onshore_wind_out)

    # Geracao Eolica Offshore ( ... -> Secundaria)
    offshore_wind_out = base_output.assign(
        technology="offshore_wind_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", offshore_wind_out)

    # Geracao Biomassa Retrofit ( ... -> Secundaria)
    biomass_retrofit_out = base_output.assign(
        technology="biomass_retrofit_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", biomass_retrofit_out)

    # Geracao Eolica Onshore ( ... -> Secundaria)
    biomass_greenfield_out = base_output.assign(
        technology="biomass_greenfield_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", biomass_greenfield_out)

    # Geracao GN Ciclo Aberto ( ... -> Secundaria)
    GN_open_cycle_out = base_output.assign(
        technology="GN_open_cycle_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", GN_open_cycle_out)

    # Geracao GN Ciclo Combinado ( ... -> Secundaria)
    GN_combined_cycle_out = base_output.assign(
        technology="GN_combined_cycle_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", GN_combined_cycle_out)

    # Geracao Hidroeletrica Grande ( ... -> Secundaria)
    large_hydroelectric_out = base_output.assign(
        technology="large_hydroelectric_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", large_hydroelectric_out)

    # Geracao Hidroeletrica Media ( ... -> Secundaria)
    medium_hydroelectric_out = base_output.assign(
        technology="medium_hydroelectric_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", medium_hydroelectric_out)

    # Geracao Carvao Nacional ( ... -> Secundaria)
    national_coal_out = base_output.assign(
        technology="national_coal_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", national_coal_out)

    # Geracao Carvao Importado ( ... -> Secundaria)
    imported_coal_out = base_output.assign(
        technology="imported_coal_ppl",
        commodity="electricity",
        level="secondary",
        value=1.0,
        unit="GWa",
    )
    scenario.add_par("output", imported_coal_out)

    return scenario, grid_efficiency