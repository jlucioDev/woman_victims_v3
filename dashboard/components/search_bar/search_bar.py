from dash import html
import dash_bootstrap_components as dbc

def create_searchbar():
    # Estilos customizados para os checkboxes e o botão
    custom_checkbox_style = {
        "margin": "0 5px",
        "borderColor": "pink"
    }

    custom_button_style = {
        "backgroundColor": "hotpink",
        "border": "none",
        "color": "white"
    }

    # Crie os checkboxes com um estilo customizado e um botão
    checklist = dbc.Checklist(
        options=[
            {"label": "IDH", "value": "IDH"},
            {"label": "PIB", "value": "PIB"},
            {"label": "GINI", "value": "GINI"},
            {"label": "IAP", "value": "IAP"},
            {"label": "Denúncias", "value": "Denuncias"}
        ],
        value=["IDH", "PIB"],  # Valores pré-selecionados
        id="multicriteria-checklist",
        inline=True,
        switch=True,  # Estiliza como switches (toggle)
        className="custom-checkbox",
        style=custom_checkbox_style
    )

    submit_button = dbc.Button(
        "CLASSIFICAÇÃO",
        id="classification-button",
        className="ml-auto",
        style=custom_button_style
    )

    # Insira os checkboxes e o botão em um CardBody
    card_body = dbc.CardBody(
        [
            html.H4("Multicritério", className="card-title"),
            checklist,
            submit_button
        ],
        className="d-flex align-items-center"  # Alinha os itens no centro
    )

    # Crie o Card e insira o CardBody
    card = dbc.Card(card_body, className="mt-3")

    return card