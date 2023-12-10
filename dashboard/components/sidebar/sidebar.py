# sidebar.py
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Defina o estado inicial da sidebar (expandida ou recolhida)
SIDEBAR_STYLE_EXPANDED = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "transition": "width 0.5s",
}

SIDEBAR_STYLE_COLLAPSED = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "3rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "transition": "width 0.5s",
}

# Botão para expandir ou recolher a sidebar
def create_sidebar_toggle():
    return dbc.Button(
        children=[html.I(className="fas fa-bars")],  # Ícone do "hamburger"
        id="sidebar-toggle",
        className="mb-2",
        color="secondary",
        style={"position": "absolute", "top": "10px", "right": "10px"},
    )

def create_sidebar():
    sidebar = html.Div(
        [
            create_sidebar_toggle(),  # Inclua o botão de alternância
            html.H2('Critérios', className='display-4'),
            html.Hr(),
            dbc.Checklist(
                options=[
                    {"label": "IDH", "value": "IDH"},
                    {"label": "PIB", "value": "PIB"},
                    {"label": "GINI", "value": "GINI"},
                    {"label": "IAP", "value": "IAP"}
                ],
                value=[],  # Valores iniciais selecionados
                id="checklist-criteria",
                inline=True
            ),
            html.Hr(),
            html.Div(id='sidebar-output-container', children=[]),
            dbc.Button('Submit', id='sidebar-submit', color='primary', className='mr-1'),
        ],
        id="sidebar",
        style=SIDEBAR_STYLE_EXPANDED,  # Estilo inicial da sidebar
    )
    return sidebar