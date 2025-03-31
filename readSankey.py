
import pandas as pd
import ixmp
from message_ix import Scenario
from message_ix.report import Reporter
from genno.operator import concat
from message_ix.tools.sankey import map_for_sankey
from pyam.figures import sankey

# Inputs
subsystems = ['N','NE','SE/CW','S']
annums = [2025] # [2025, 2030, 2035]

mp = ixmp.Platform()                                                        # Connect to the ixmp platform
scenario = Scenario(mp, model="Brasil Electrified", scenario="baseline")    # Load the scenario

for subsystem in subsystems:
    for annum in annums:
        # Create Sankey diagram for each subsystem and year
        rep = Reporter.from_scenario(scenario, units={"replace": {"-": ""}}) # Remove "-" from units
        df_all = concat(rep.get("in::pyam"), rep.get("out::pyam"))           # Concatenate input and output dataframes
        df = df_all.filter(year=annum, region=subsystem+'|'+subsystem)       # Filter for the year and subsystem
        mapping = map_for_sankey(df, node=subsystem,)                        # Map the data for Sankey diagram
        fig = sankey(df=df, mapping=mapping)                                 # Create the Sankey diagram
        fig.show()

mp.close_db()
