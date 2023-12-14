import plotly.express as px



def create_linear_graph(df):
    # Converter colunas de casos para formato longo
    df_melted = df.melt(id_vars=["id", "localidade"], 
                        value_vars=[f'qty_casos_{year}' for year in range(2014, 2024)],
                        var_name="Ano", 
                        value_name="Casos")

    # Converter Ano para formato numérico removendo 'qty_casos_'
    df_melted['Ano'] = df_melted['Ano'].str.replace('qty_casos_', '').astype(int)

    # Criar o gráfico de linhas
    fig = px.line(df_melted, x="Ano", y="Casos", color='localidade', 
              title='Histórico Anual de Casos de Violência')

    # Atualizando o layout para usar a largura total
    fig.update_layout(
        autosize=True,
        width=1000,  # Pode precisar ajustar de acordo com a largura da tela do usuário
        margin=dict(l=20, r=20, t=40, b=20)  # Reduzir as margens se necessário
    )
    return fig