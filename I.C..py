import os
import re
import pandas as pd


# Diretório com os arquivos
base_dir = "./" 
file_pattern = re.compile(r"GERACAO_USINA-2_\d{4}_\d{2}\.parquet")

# Agrupar dados de todos os arquivos
all_data = pd.DataFrame()
for file in os.listdir(base_dir):
    if file_pattern.match(file):
        path = os.path.join(base_dir, file)
        df = pd.read_parquet(path)
        all_data = pd.concat([all_data, df], ignore_index=True)

# Verificações de nomes de colunas esperadas
required_cols = {"id_ons", "val_geracao", "din_instante", "nom_tipousina", "nom_usina", "id_estado"}
missing = required_cols - set(all_data.columns)
if missing:
    raise ValueError(f"Colunas faltando no dataset: {missing}")

# Conversão de data e ordenação
all_data['din_instante'] = pd.to_datetime(all_data['dth_referencia'])
all_data.sort_values(by=['id_ons', 'din_instante'], inplace=True)

# Intervalo de 4 horas
sampled = all_data.set_index('din_instante').groupby('id_ons').resample('4H')['val_geracao'].mean().reset_index()

# Cálculo dos ramp_ups e ramp_downs por usina
def calc_ramps(group):
    diff = group['val_geracao'].diff()
    ramp_up = diff.max()
    ramp_down = -diff.min()
    return pd.Series({'ramp_up': ramp_up, 'ramp_down': ramp_down})

ramps = sampled.groupby('id_ons').apply(calc_ramps).reset_index()

# P_min e P_max
cap = all_data.groupby('id_ons')['val_geracao'].agg(P_min='min', P_max='max').reset_index()

# Junta ramps e capacidade
merged = pd.merge(cap, ramps, on='id_ons')

# Junta metadados (nome, tipo, regiao)
meta_cols = ['id_ons', 'nom_usina', 'nom_tipousina', 'id_estado']
meta = all_data[meta_cols].drop_duplicates(subset='id_ons')
final = pd.merge(merged, meta, on='id_ons')

#Δt = 4 (horas)
delta_t = 4

# Flex
final['flexibilidade'] = (
    (0.5 * (final['P_max'] - final['P_min']) + 0.5 * final['ramp_up'] * delta_t) / final['P_max']
).round(4)

# Organiza colunas e nomes
final = final[['id_estado', 'nom_usina', 'nom_tipousina', 'flexibilidade',
               'ramp_up', 'ramp_down', 'P_min', 'P_max']]

final.columns = ['regiao', 'usina', 'tipo', 'flexibilidade',
                 'ramp_ups', 'ramp_downs', 'capacidade_minima', 'capacidade_maxima']

# Exporta para o Excel
final.to_excel("flexibilidade_usinas.xlsx", index=False)
print("Arquivo 'flexibilidade_usinas.xlsx' criado com sucesso.")
