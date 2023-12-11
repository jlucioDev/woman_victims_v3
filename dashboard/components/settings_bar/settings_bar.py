from dash import html, dcc
import dash_bootstrap_components as dbc


def create_settingsbar():

    header_style = {
    "backgroundColor": "white",  # Cor de fundo cinza do cabeçalho do card
    "borderTopLeftRadius": "0.25rem",
    "borderTopRightRadius": "0.25rem",
    "color": "#E964A1",  # Texto branco
    #"padding": "0.75rem 1.25rem",
    "marginBottom": "0",  # Remove a margem inferior
    "borderBottom": "none"  # Remove a borda inferior
    }
    
    custom_button_style = {
        "backgroundColor": "hotpink",
        "border": "none",
        "color": "white"
    }

    

    def submit_button():
        return dbc.Button(
        "CLASSIFICAÇÃO",
        id="classification-button",
        className="ml-auto",
        style=custom_button_style
    )

    def multicrit_dropdown():
        return dcc.Dropdown(
            options=[
                {'label': 'IDH', 'value': 'IDH'},
                {'label': 'PIB', 'value': 'PIB'},
                {'label': 'GINI', 'value': 'GINI'},
                {'label': 'IAP', 'value': 'IAP'}
            ],
            value=['IDH', 'PIB', 'GINI', 'IAP'],
            id='memory-criteria',
            multi=True,
            className="mb-1"
        )

    def classifier_dropdown():
        return dcc.Dropdown(
            options=[
                {'label': 'Random Florest Classifier', 'value': 'RandFloClass'},
                {'label': 'Quantile Classifier', 'value': 'QuantClass'}
            ],
            value='RandFloClass',
            id='memory-classifier',
            className="mb-1"
        )

    card_body = dbc.CardBody(
        [
            dbc.Col(
                children=[
                    html.Div("Configurações", style=header_style),
                    multicrit_dropdown(),
                    classifier_dropdown(),
                    submit_button(),
                ],
                width=12)
            
        ]
    )


    # Crie o Card e insira o CardBody
    card = dbc.Card(card_body, className="mt-3")

    return card
