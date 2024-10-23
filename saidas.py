# Modulo Saidas

def gera_excel(pd,scenario):
    # Gera saidas Excel
    # ^^^^^^^^^^^^^^^^^

    b = pd.DataFrame(scenario.var("CAP"))
    b.to_excel("Capacidade.xlsx")
    
    c = pd.DataFrame(scenario.var("CAP_NEW"))
    c.to_excel("Nova Capacidade das Instalações.xlsx")

    d = pd.DataFrame(scenario.var("ACT"))
    d.to_excel("Atividade.xlsx")

    return None