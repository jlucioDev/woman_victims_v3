import plotly.express as px


def create_map(df, municipios_json):
    # Criando o mapa usando Plotly Express
    fig = px.choropleth_mapbox(
        df,
        geojson=municipios_json,
        locations='id',  # Usando o ID do dataframe
        featureidkey="properties.id",
        color='CLASS',  # Usando a coluna 'class' do dataframe
        color_continuous_scale=px.colors.sequential.PuRd,  # Escala de cores em tons de laranja
        range_color=(0, df['CLASS'].max()),  # Intervalo de cores baseado na coluna 'class'
        opacity=0.7,
        #mapbox_style="carto-positron",
        mapbox_style="white-bg", 
        hover_name="localidade",  # Definindo 'localidade' como o texto principal no hover
        hover_data={"id": False, "CLASS": False, "IDH": False, "IAP": False},  # Ocultando 'id', 'class', 'IDH' e 'IAP' no hover
        zoom=4.5,
        center={"lat": -3.53, "lon": -52.29}
    )
    # Atualizando o layout para remover as bordas
    fig.update_geos(fitbounds="locations")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    #return dcc.Graph(id='mapa-municipios', figure=fig)
    return fig