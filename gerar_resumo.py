import pandas as pd

print("1. Lendo arquivo original...")
df = pd.read_parquet("data_gas_otimizado.parquet")

print("2. Criando tabelas de resumo...")

# Tabela 1: Médias por Ano/Estado (Para os gráficos de barra)
df_barras = df.groupby(['ANO', 'REGIÃO', 'ESTADO'])['VALOR REVENDA (R$/L)'].mean().reset_index()
df_barras.to_csv("resumo_barras.csv", index=False)

# Tabela 2: Máximos e Mínimos por Ano (Para o gráfico de cima)
df_maxmin = df.groupby(['ANO'])['VALOR REVENDA (R$/L)'].agg(['max', 'min']).reset_index()
df_maxmin.to_csv("resumo_maxmin.csv", index=False)

# Tabela 3: Dados para o Gráfico de Linha (Agrupado por Mês para ficar leve)
df['DATA'] = pd.to_datetime(df['DATA'])
df['MES_ANO'] = df['DATA'].dt.to_period('M').astype(str)
df_linha = df.groupby(['MES_ANO', 'ESTADO'])['VALOR REVENDA (R$/L)'].mean().reset_index()
df_linha.to_csv("resumo_linha.csv", index=False)

print("SUCESSO! 3 arquivos pequenos foram criados: resumo_barras.csv, resumo_maxmin.csv e resumo_linha.csv")