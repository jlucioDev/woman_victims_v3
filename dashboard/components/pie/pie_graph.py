import plotly.express as px



def create_pie(df):
    class_colors = {
        0: '#F9F7FB',
        1: '#DBC9E2',
        2: '#E964A1',
        3: '#954D62',
    }
    df['risk_description'] = df['class'].map({
        0: 'Risco Baixo',
        1: 'Risco Médio',
        2: 'Risco Alto',
        3: 'Risco Muito Alto'
    })

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
        #autosize=True,
        width=500,  # Largura em pixels
        height=300,  # Altura em pixels
        
        # Posicionamento da legenda
        legend=dict(
            title='',  # Remova o título da legenda
            orientation='h',  # Legenda horizontal
            yanchor="bottom",
            y=-0.50,  # Posição Y da legenda
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
        marker=dict(line=dict(color='#000000', width=0))  # Borda preta nas fatias do gráfico
    )

    #return dcc.Graph(id='pie-chart', figure=pie_fig)
    return pie_fig