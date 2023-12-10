import json
import dash
from dash import html, State, Input, Output
import plotly.express as px
import pandas as pd
from layout import create_layout
from components.map.map_graph import create_map
from components.pie.pie_graph import create_pie
from components.sidebar.sidebar import create_sidebar, SIDEBAR_STYLE_EXPANDED, SIDEBAR_STYLE_COLLAPSED
from components.search_bar.search_bar import create_searchbar
import dash_bootstrap_components as dbc

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
            create_searchbar,
            create_map(df, municipios), 
            create_pie(df)
        ),
        #create_sidebar()
    ]
)
# Callback para alternar a sidebar
# @app.callback(
#     Output("sidebar", "style"),
#     [Input("sidebar-toggle", "n_clicks")],
#     [State("sidebar", "style")],
# )
# def toggle_sidebar(n_clicks, style):
#     if n_clicks:
#         if style and style["width"] == SIDEBAR_STYLE_EXPANDED["width"]:
#             # Sidebar está expandida, então recolha
#             return SIDEBAR_STYLE_COLLAPSED
#         else:
#             # Sidebar está recolhida, então expanda
#             return SIDEBAR_STYLE_EXPANDED
#     # Se n_clicks é None (não clicado ainda), retorne o estilo que foi passado para a função
#     return style

# # Callback para atualizar a lista com a seleção do usuário
# @app.callback(
#     Output('sidebar-output-container', 'children'),
#     [Input('sidebar-submit', 'n_clicks')],
#     [State('checklist-criteria', 'value')],
# )
# def update_output(n_clicks, selected_criteria):
#     if n_clicks:
#         return html.Ul([html.Li(criteria) for criteria in selected_criteria])
    
# Callback para atualizar as informações
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
    else:
        print("ClickData is None")  # Imprime para depuração
    # Caso nenhum município esteja clicado, retorna informações vazias
    return ("IDH:", "PIB:", "GINI:", "IAP (Índice de Ass. Proteção):", "Classificação", 'Clique em um município')



       

# Executando o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
