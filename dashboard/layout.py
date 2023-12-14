
from dash import html, dcc
import dash_bootstrap_components as dbc

# Camada de estilos
# Estilo para o cabeçalho do card
header_style = {
    "backgroundColor": "white",  # Cor de fundo cinza do cabeçalho do card
    "borderTopLeftRadius": "0.25rem",
    "borderTopRightRadius": "0.25rem",
    "color": "#E964A1",  # Texto branco
    "padding": "0.75rem 1.25rem",
    "marginBottom": "0",  # Remove a margem inferior
    "borderBottom": "none"  # Remove a borda inferior
}

# Estilo para o corpo do card
body_style = {
    "padding": "1.25rem",  # Espaçamento interno do card
    "backgroundColor": "white"  # Cor de fundo claro para o corpo do card
    #"color": "#954D62"
}

# Estilo para o rodapé do card
footer_style = {
    "padding": "0.75rem 1.25rem",  # Espaçamento interno do rodapé
    "backgroundColor": "#f8f9fa",  # Cor de fundo claro para o rodapé
    "borderTop": "1px solid #dee2e6",  # Borda superior
    "color": "#6c757d"  # Cor do texto cinza
}



#Cria o layout da aplicação
def create_layout(searchbar, fig_map, pie_fig, fig_annual):
    # Chame a função para criar a barra de pesquisa
    search_bar_component = searchbar()

    # Titulo da Aplicação
    markdown_title = '''
        ### **Dashboard** - Violência Contra a Mulher em  Municípios Paraenses.


        Apresentação das informações de dados de violência e classificação com método multicritério ELECTRE Tri-b.

    '''

    # Container principal do layout
    layout = dbc.Container(
        [
            dbc.Row(

                dcc.Markdown(children=markdown_title)
                
            ),
            # Linha de pesquisa aqui
            dbc.Row(
                dbc.Col(search_bar_component, width=12),  # Certifique-se de ajustar a largura conforme necessário
                className='mb-4'
            ),
            
            # Linha com dois Cards
            dbc.Row(
                [   
                    # Primeira Coluna
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                dcc.Loading(
                                    id="loading-pieChart",
                                    type="default",
                                    children=[html.Div( 
                                        dcc.Graph(id='pie-chart', figure=pie_fig),
                                        style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'})
                                    ],  # Esta div será atualizada após a classificação
                                )
                            ),
                            className="h-100"
                        ),
                        md=3
                    ),
                    # Coluna para o mapa
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                dcc.Loading(
                                    id="loading-mapChart",
                                    type="default",  # Você pode escolher entre 'graph', 'cube', 'circle', 'dot', ou 'default'
                                    children=[
                                        html.Div(id="loading-output-1"),
                                        dcc.Graph(id='mapa-municipios', figure=fig_map)
                                    ],
                                ),
                            ),
                            className="h-60"
                        ),
                        md=6  # Tamanho da coluna para o mapa
                    ),
                    # Coluna para informações do município
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div("Dados do Município de Óbidos", style=header_style),
                                    html.P("IDH:", id="info_idh", className="card-text"),
                                    html.P("PIB:", id="info_pib", className="card-text"),
                                    html.P("IAP (Índice de Ass. Proteção):", id="info_iap", className="card-text"),
                                    html.P("GINI:", id="info_gini", className="card-text"),
                                    html.Hr(),
                                    html.P("Classificação:", id="info_class", className="card-text"),
                                    html.P("Registros de ocorrência de VCM:", id="", className="card-text"),
    
                                    html.Div(id='info-municipio')
                                ]  # Placeholder para as informações do município
                            ),
                            className="h-60"
                        ),
                        md=3  # Tamanho da coluna para as informações
                    ),
                ],
                className="mt-40 mb-4",  # Espaçamento entre as colunas
            ),
            dbc.Row(
                dbc.Card(
                    dbc.CardBody(
                        dcc.Loading(
                            id="loading-LinearChart",
                            type="default",
                            children=[html.Div(
                                dcc.Graph(id='annual-violence-chart', figure=fig_annual),
                                style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'})
                            ],  # Esta div será atualizada após a classificação
                        )
                    ),
                ),
                className="mx-2 mt-10 mb-4"  # Classe para margem externa lateral de 20 e superior de 40
            )
        ],
        fluid=True,
    )

    return layout

   

