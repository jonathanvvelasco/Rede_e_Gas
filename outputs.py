# Module Outputs

def generate_excel(pd,scenario):
    # Create Excel outputs
    # ^^^^^^^^^^^^^^^^^

    b = pd.DataFrame(scenario.var("CAP"))
    b.to_excel("Capacity.xlsx")
    
    c = pd.DataFrame(scenario.var("CAP_NEW"))
    c.to_excel("New Capacity.xlsx")

    d = pd.DataFrame(scenario.var("ACT")).pivot_table(index="technology", columns="year_act", values="lvl", aggfunc="sum")
    d.to_excel("Activity.xlsx")

    return None
