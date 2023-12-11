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
            dcc.Store(id='dataset', data=df.to_dict('records')),  # Armazenar os dados do DataFrame
    
        ),
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
)

def display_click_data(clickData):
    if clickData is not None:
        # Ajuste para corresponder ao id no dataframe
        id_municipio = clickData['points'][0]['location']
        # Aqui, buscamos o nome do município usando o ID ajustado no dataframe
        municipio_info = df[df['id'] == id_municipio].iloc[0]
         # Atualiza as divs com as informações
        return (
            f"IDH: {municipio_info['IDH']}",
            f"PIB: {municipio_info['PIB']}",
            f"GINI: {municipio_info['GINI']}",
            f"IAP (Índice de Ass. Proteção): {municipio_info['IAP']}",
            f"Classificação: {municipio_info['class']}",
            f"ID: {municipio_info['id']}, Nome: {municipio_info['localidade']}"
        )

    # Caso nenhum município esteja clicado, retorna informações vazias
    return ("IDH:", "PIB:", "GINI:", "IAP (Índice de Ass. Proteção):", "Classificação", 'Clique em um município')


# Callback para classificar os dados.
@app.callback(
    Output('mapa-municipios', 'figure'),  # substitua por um componente de saída adequado em seu layout
    Input('classification-button', 'n_clicks'),
    State('memory-criteria', 'value'),
    State('memory-classifier', 'value'),
    prevent_initial_call=True  # Evita que o callback seja disparado na inicialização
)
def classify_update_map(n_clicks, selected_criteria, selected_type):
    
    # Executa alguma ação aqui quando o botão for clicado
    print(f'Botão clicado! {n_clicks}')

    # Validação
    if len(selected_criteria) > 2:
        
        
        # Recebe a nova coluna de classificação
        c = classifierModel('pa')
        cl = c.create_classification(df, selected_criteria, selected_type)
        df['class'] = cl
        create_map(df, municipios)
        print(" ---  Mapa Recriado!")

       
        # Altera o DataFrame

        # Recria o gráfico com o dataFrame atualizado.


# Executando o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
