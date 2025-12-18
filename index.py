import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import os
from app import *

# ===== CARREGAMENTO DOS DADOS ====== #
# Usando o arquivo parquet que você já tem no GitHub por ser mais rápido
try:
    df_barras = pd.read_csv("resumo_barras.csv")
    df_maxmin = pd.read_csv("resumo_maxmin.csv")
    
    # Converter colunas para garantir compatibilidade
    df_barras['ANO'] = df_barras['ANO'].astype(str)
    df_maxmin['ANO'] = df_maxmin['ANO'].astype(str)
except Exception as e:
    print(f"Erro ao carregar arquivos: {e}")
    df_barras = pd.DataFrame(columns=['ANO', 'REGIÃO', 'ESTADO', 'VALOR REVENDA (R$/L)'])
    df_maxmin = pd.DataFrame(columns=['ANO', 'max', 'min'])

# Criando as listas usando .tolist() para evitar o erro de valor ambíguo (Linha 39)
if not df_barras.empty:
    anos_disp = sorted(df_barras['ANO'].unique().tolist())
    regioes_disp = df_barras['REGIÃO'].unique().tolist()
else:
    anos_disp = []
    regioes_disp = []

val_ano = anos_disp[0] if anos_disp else ""
val_regiao = regioes_disp[0] if regioes_disp else ""

# ===== LAYOUT DO DASHBOARD ====== #
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Gasolina Dashboard", style={"font-weight": "bold"}),
                    html.P("Análise de Preços ANP"),
                    html.Hr(),
                    dbc.Button("Voltar ao Portfólio", href="https://visiondatapro.com", size="sm")
                ])
            ], style={'height': '100vh', 'margin': '10px', 'padding': '20px'})
        ], md=3),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5('Máximos e Mínimos por Ano'),
                            dcc.Graph(id='static-maxmin')
                        ])
                    ])
                ], md=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Filtro de Ano:'),
                            dcc.Dropdown(id="select_ano", value=val_ano, options=[{"label": x, "value": x} for x in anos_disp]),
                            html.H6('Filtro de Região:', style={'margin-top': '20px'}),
                            dcc.Dropdown(id="select_regiao", value=val_regiao, options=[{"label": x, "value": x} for x in regioes_disp]),
                        ])
                    ])
                ], md=6)
            ])
        ], md=9)
    ])
], fluid=True)

# Define o servidor para o Gunicorn (Railway) ler
server = app.server

if __name__ == '__main__':
    # Railway fornece a porta automaticamente
    port = int(os.environ.get("PORT", 8080))
    app.run_server(host='0.0.0.0', port=port)
