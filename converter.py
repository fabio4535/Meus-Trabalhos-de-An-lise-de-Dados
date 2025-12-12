import pandas as pd

print("1. Lendo CSV...")
# Lê o arquivo
df = pd.read_csv("data_gas.csv", low_memory=False)

# === CORREÇÃO MÁGICA DE COLUNAS ===
# Remove espaços vazios antes e depois dos nomes das colunas
# Ex: transforma ' DATA INICIAL' em 'DATA INICIAL'
df.columns = df.columns.str.strip()

print("   Colunas encontradas no arquivo:")
print(list(df.columns))
# ==================================

# 2. Seleciona as colunas (Agora usando os nomes SEM espaços)
colunas_uteis = [
    'DATA INICIAL', 'DATA FINAL', 'PREÇO MÉDIO REVENDA', 
    'PRODUTO', 'ESTADO', 'REGIÃO'
]

print("2. Filtrando colunas úteis...")
try:
    df = df[colunas_uteis]
except KeyError as e:
    print("\nERRO: Ainda não encontrei as colunas certas.")
    print(f"O computador procurou por: {colunas_uteis}")
    print("Mas o arquivo tem outros nomes. Verifique a lista impressa acima.")
    exit()

# 3. Filtra só Gasolina
print("3. Filtrando Gasolina...")
df = df[df['PRODUTO'] == 'GASOLINA COMUM']

# 4. Tratamento de dados
print("4. Otimizando tipos de dados...")
df['DATA INICIAL'] = pd.to_datetime(df['DATA INICIAL'], errors='coerce')
df['DATA FINAL'] = pd.to_datetime(df['DATA FINAL'], errors='coerce')
df['DATA MEDIA'] = ((df['DATA FINAL'] - df['DATA INICIAL'])/2) + df['DATA INICIAL']
df.rename(columns = {'DATA MEDIA':'DATA'}, inplace = True)
df.rename(columns = {'PREÇO MÉDIO REVENDA': 'VALOR REVENDA (R$/L)'}, inplace=True)
df["ANO"] = df["DATA"].apply(lambda x: str(x.year) if pd.notnull(x) else "")
df['VALOR REVENDA (R$/L)'] = pd.to_numeric(df['VALOR REVENDA (R$/L)'], errors='coerce')

# 5. Salva em PARQUET
print("5. Salvando arquivo otimizado...")
df.to_parquet("data_gas_otimizado.parquet", index=False)
print("\nSUCESSO! Arquivo 'data_gas_otimizado.parquet' criado.")
print("Agora faça o upload dele para o GitHub!")