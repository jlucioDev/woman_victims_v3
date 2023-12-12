import json
import dash
from dash import html, dcc, State, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from layout import create_layout
from components.map.map_graph import create_map
from components.pie.pie_graph import create_pie
from components.settings_bar.settings_bar import create_settingsbar
from classifier.classifier_model import classifierModel
from dash.exceptions import PreventUpdate


# Carregando o arquivo GeoJSON
with open('dashboard/components/map/munics_modified.geojson') as geo:
    municipios = json.load(geo)

# Carregando o dataset com os municípios classificados
df = pd.read_parquet('datasets/df_classified_pa.parquet')

# Inicializando a aplicação Dash com o tema do Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Configurando o layout da aplicação usando a função importada
app.layout = html.Div(
    [
        
        create_layout(
            create_settingsbar,
            create_map(df, municipios), 
            create_pie(df),
        ),
        dcc.Store(id='dataset', data=df.to_dict('records')),  # Armazenar os dados do DataFrame
    
    ]
)

    
# Callback para atualizar as informações ao clicar no mapa
@app.callback(
    [
        Output('info_idh', 'children'),
        Output('info_pib', 'children'),
        Output('info_gini', 'children'),
        Output('info_iap', 'children'),
        Output('info-municipio', 'children'),
        Output('info_class', 'children'),
    ],
    [Input('mapa-municipios', 'clickData')],
    [State('dataset', 'data')] 
   
)

def display_click_data(clickData, stored_data):
    if clickData is not None:
        
        # Ajuste para corresponder ao id no dataframe
        id_municipio = clickData['points'][0]['location']

        # Converta os dados armazenados de volta para um DataFrame
        df_atualizado = pd.DataFrame(stored_data)
        
        # Aqui, buscamos o nome do município usando o ID ajustado no dataframe
        municipio_info = df_atualizado[df_atualizado['id'] == id_municipio].iloc[0]
         # Atualiza as divs com as informações
        return (
            f"IDH: {municipio_info['IDH']}",
            f"PIB: {municipio_info['PIB']}",
            f"GINI: {municipio_info['GINI']}",
            f"IAP (Índice de Ass. Proteção): {municipio_info['IAP']}",
            f"Classificação: {municipio_info['CLASS']}",
            f"ID: {municipio_info['id']}, Nome: {municipio_info['localidade']}"
        )

    # Caso nenhum município esteja clicado, retorna informações vazias
    return ("IDH:", "PIB:", "GINI:", "IAP (Índice de Ass. Proteção):", "Classificação", 'Clique em um município')


# Callback para classificar os dados e atualizar o mapa, gráfico de pizza e o dcc.Store.
@app.callback(
    [
     Output('mapa-municipios', 'figure'),
     Output('pie-chart', 'figure'),
     Output('dataset', 'data'),
    ],
    [Input('classification-button', 'n_clicks')],
    [State('memory-criteria', 'value'),
     State('memory-classifier', 'value'),
     State('dataset', 'data')]
)

def classify_update_map(n_clicks, selected_criteria, selected_type, df_data):
    if n_clicks is None:
        raise PreventUpdate

    if len(selected_criteria) >= 2:
        c = classifierModel('pa')
        df_data = pd.DataFrame(df_data)

        cl = c.create_classification(df_data, selected_criteria, selected_type)
        df_data['CLASS'] = cl

        updated_map = create_map(df_data, municipios)
        updated_pie_chart = create_pie(df_data)

        # Atualize os dados no dcc.Store
        return updated_map, updated_pie_chart, df_data.to_dict('records')

    else:
        raise PreventUpdate


# Executando o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
