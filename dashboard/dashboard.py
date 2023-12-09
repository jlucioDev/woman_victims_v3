import json
import dash
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from layout import create_layout 
import dash_bootstrap_components as dbc

# Mapeamento das cores para cada classificação
class_colors = {
    0: '#F9F7FB',  # Classe 0
    1: '#DBC9E2',  # Classe 1
    2: '#E964A1',  # Classe 2
    3: '#954D62',  # Classe 3
}

# Crie um dicionário para mapear os valores numéricos para as descrições de risco
risk_description = {
    3: "Risco Muito Alto",
    2: "Risco Alto",
    1: "Risco Médio",
    0: "Risco Baixo"
}

# Carregando o arquivo GeoJSON
with open('munics_modified.geojson') as geo:
    municipios = json.load(geo)

# Carregando o dataset com os municípios classificados
df = pd.read_parquet('datasets/df_classified_pa.parquet')

# Atualize o dataframe para incluir uma nova coluna com as descrições de risco
df['risk_description'] = df['class'].map(risk_description)


# Calcula a contagem de cada classificação
class_counts = df['class'].value_counts().reset_index()
class_counts.columns = ['class', 'count']

# Inicializando a aplicação Dash com o tema do Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Criando o mapa usando Plotly Express
fig = px.choropleth_mapbox(
    df,
    geojson=municipios,
    locations='id',  # Usando o ID do dataframe
    featureidkey="properties.id",
    color='class',  # Usando a coluna 'class' do dataframe
    color_continuous_scale=px.colors.sequential.PuRd,  # Escala de cores em tons de laranja
    range_color=(0, df['class'].max()),  # Intervalo de cores baseado na coluna 'class'
    opacity=0.7,
    #mapbox_style="carto-positron",
    mapbox_style="white-bg", 
    hover_name="localidade",  # Definindo 'localidade' como o texto principal no hover
    hover_data={"id": False, "class": False, "IDH": False, "IAP": False},  # Ocultando 'id', 'class', 'IDH' e 'IAP' no hover
    zoom=4.5,
    center={"lat": -3.53, "lon": -52.29}
)
# Atualizando o layout para remover as bordas
fig.update_geos(fitbounds="locations")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Criando o gráfico de pizza com Plotly Express
pie_fig = px.pie(
    df,
    names='risk_description',
    title='Distribuição de Riscos',
    color='class',
    #color_discrete_sequence=px.colors.sequential.PuRd,
    color_discrete_map=class_colors,
)

# Configurações de layout para aumentar o tamanho e posicionar a legenda
pie_fig.update_layout(
    # Tamanho do gráfico
    autosize=True,
    #width=500,  # Largura em pixels
    #height=300,  # Altura em pixels
    
    # Posicionamento da legenda
    legend=dict(
        title='',  # Remova o título da legenda
        orientation='h',  # Legenda horizontal
        yanchor="bottom",
        y=-0.25,  # Posição Y da legenda
        xanchor="right",
        x=1  # Posição X da legenda
    ),
    
    # Remova o fundo e bordas do gráfico
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color="black"  # Cor do texto
)

# Atualizar os traços do gráfico para alterar o texto do hover
pie_fig.update_traces(
    textinfo='percent',  # Mostrar apenas a porcentagem
    hoverinfo='label+percent',  # Mostrar o rótulo personalizado e a porcentagem no hover
    marker=dict(line=dict(color='#000000', width=1))  # Borda preta nas fatias do gráfico
)
# Configurando o layout da aplicação usando a função importada
app.layout = create_layout(fig, pie_fig)

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
    # Caso nenhum município esteja clicado, retorna informações vazias
    return ("IDH:", "PIB:", "GINI:", "IAP (Índice de Ass. Proteção):", "Classificação", 'Clique em um município')



       

# Executando o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
