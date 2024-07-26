import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


################################## Dados Úteis ############################################## 
# Cores NMC
roxo = "#521C78"
laranja = "#F0A800"
azul = "#121C4D"
azul_b = "#14A2dc"
vermelho = "#E8501C"
verde = "#198036"
amarelo = "#DDD326"
cinza = "#888DA6"
paleta_IVS = [azul_b,azul, amarelo, laranja, vermelho]
paleta_NMC = [roxo, laranja, azul, vermelho, azul_b, verde,amarelo]


################################## FUNÇÕES ÚTEIS #######################################
# treemap
def plot_treemap(df, col, index=True):
    if index==True:
        parents = ['']*len(df.index)
        fig = go.Figure(go.Treemap(
            labels =df.index, values=df[col], parents=parents
        ))
        fig.update_traces(marker=dict(cornerradius=5))
        fig.update_layout(
            treemapcolorway = paleta_NMC)
    return fig

#Filtrar datas do dataframe através do widget date_input
def filtrar_data(df, col, data):
    if len(data)>1:
        data_ini = data[0]
        data_fim = data[1]
        df_f = df.loc[(df[col].dt.date >= data_ini)&
                    (df[col].dt.date <= data_fim)]
        return df_f
    
    elif len(data)==1:
        data_ini = data[0]
        df_f = df.loc[(df[col].dt.date >= data_ini)]
        return df_f
        
    return df_f


# Tabela dinâmica
def criar_tabela_agregada(df, agrupador, coluna_calculo, tipo_calculo, novo_nome=None,drop=True):
    import streamlit as st
    df = df.groupby(agrupador, dropna=drop).agg({coluna_calculo:tipo_calculo}).reset_index()
    df['Percentual'] = round((df[coluna_calculo]/sum(df[coluna_calculo])).astype(float)*100, 2)
    if novo_nome is not None:
        df = df.rename(columns=novo_nome)
    else:
        pass
    df = df.sort_values(by='Percentual', ascending=False)

    return df

# Gráfico de barras
# @st.cache_data()
def px_bar_chart(df, x_axis, y_axis, title='', orientacao=None,cor=roxo, texto=False, tooltip=None, largura=None, altura = None, **kwargs):
    fig = px.bar(df, x=x_axis,
                 y=y_axis,
                 title = title,
                 color_discrete_sequence = [cor], 
                 orientation=orientacao,
                 text_auto=texto,
                 hover_data=[tooltip],
                 height=altura,
                 width=largura, **kwargs)
    

    return fig

# Pirâmide Etária Um plot
def piramide_etaria(faixa, coluna_masculino, coluna_femino):
    homens = coluna_masculino
    mulheres = coluna_femino*-1

    y = faixa

    layout = go.Layout(yaxis=go.layout.YAxis(title='Idade'),
                    xaxis= go.layout.XAxis(
                                    range=[min(mulheres), max(homens)],
                                    tickvals=[np.array(mulheres),np.array(homens)],
                                    ticktext=[np.array(mulheres)*-1,np.array(homens)]
                                            ),
        barmode='overlay',
        bargap=0.1

    )

    data = [
        go.Bar(y=y,
            x=homens,
            orientation='h',
            name='Masculino',
            text=homens.astype(int),
            hoverinfo='text',
            marker=dict(color=azul)               
        ),
        go.Bar(y=y,
            x=mulheres,
            orientation='h',
            name='Feminino',
            text=mulheres.astype(int)*-1,
            hoverinfo='text',
            marker=dict(color=roxo)
            )
    ]
    
    fig = dict(data=data, layout=layout)

    return fig

# Piramide Etaria dois plot
def piramide_etaria_dois_plot(faixa, coluna_masculino, coluna_femino, coluna_masc_2=None, coluna_fem_2=None):
    men_one = coluna_masculino
    men_two = coluna_masc_2
    woman_one = coluna_femino*-1
    woman_two = coluna_fem_2 *-1

    y = faixa

    layout = go.Layout(yaxis=go.layout.YAxis(title='Idade'),
                    xaxis=go.layout.XAxis(
                        range=[min(woman_one), max(men_one)],
                        tickvals=[np.array(woman_one),np.array(men_one)],
                        ticktext=[np.array(woman_one)*-1,np.array(men_one)],
                        title='Valores'),
                    barmode='overlay',
                    bargap=0.1)

    data = [go.Bar(y=y,
                x=men_one,
                orientation='h',
                name='Masculino População',
                hoverinfo='x',
                marker=dict(color=azul_b)
                ),
            go.Bar(y=y,
                x=woman_one,
                orientation='h',
                name='Feminino População',
                hoverinfo='x',
                marker=dict(color=roxo)
                ),
            go.Bar(y=y,
                x=men_two,
                orientation='h',
                name = 'Masculino Rais',
                hoverinfo='x',
                showlegend=True,
                opacity=0.5,
                marker=dict(color=verde)
                ),
            go.Bar(y=y,
                x=woman_two,
                orientation='h',
                name='Feminino Rais',
                hoverinfo='x',
                showlegend=True,
                opacity=0.5,
                marker=dict(color=amarelo)
                )]
    fig = dict(data=data, layout=layout)

    return fig

# Pie Chart
def grafico_rosca(df, valores, fatias, nome=None, circulo=None, cor=None, title_text=''):
    label = df[fatias]
    valor = df[valores]

    fig = go.Figure()

    fig.add_trace(go.Pie(labels=label,
                         values=valor,
                         name=nome))
    
    fig.update_traces(
        hole = circulo,
        hoverinfo="label+percent+name",
        marker = dict(colors=cor)
    )
    fig.update_layout(
        title_text= title_text
    )

    return fig


# Criação de cards
def metric_custom(titulo_box, valor_box, cor_caixa='#7ED1EF', cor_font='white', fontsize=50, iconname="fa-solid fa-venus"):
    cor_caixa = cor_caixa
    cor_font = cor_font
    fontsize = fontsize
    iconname = iconname
    titulo_box = titulo_box
    
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v6.3.0/css/all.css" crossorigin="anonymous">'
    
    valor_box = valor_box
    
    htmlstr = f"""<p style='background-color:{cor_caixa};
    color:{cor_font};
    font-size: {fontsize}px;
    border-radius: 7px;
    padding-left: 12px;
    padding-top: 18px;
    padding-bottom: 18px;
    line-height:25px;'>
    <i class='{iconname} fa-xs'></i> {valor_box}
    </style><BR><span style='font-size: 14px;
    margin-top: 0;'>{titulo_box}</style></span></p>"""
    
    return lnk + htmlstr

# Gráfico de Linha
def grafico_linha(df, x_axis, y_axis, titulo = None, rotulo=None, cor = None, local_rotulo=None):
    fig = px.line(df, x=x_axis, 
                  y=y_axis, 
                  title=titulo,
                  color=cor, 
                  text = rotulo)

    fig.update_traces(textposition=local_rotulo)

    return fig

def grafico_area(df, x_axis, y_axis, cor=None, area=None, simbolo = None):
    fig = px.area(df, 
                  x=x_axis,
                  y=y_axis,
                  color = cor,
                  line_group=area, 
                  pattern_shape_sequence=simbolo)
    
    return fig

def indicator_chart(valor, limite,titulo=None):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
        mode='gauge+number',
        value=valor,
        title = titulo,
        domain= {'x' : [0,1], 'y': [0,1]},
        gauge={
            'axis': {
                'range' : [0,limite]
            }
        }
        )
    )

    return fig

@st.cache_data()
def histograma(nome_coluna, coluna, x_axis = None, y_axis = None, titulo_y=None, cor=roxo, legenda =False, caixas=None, largura=None, altura=None):
    df_ = pd.DataFrame({nome_coluna: coluna})

    fig = px.histogram(df_, x=x_axis,
                       y=y_axis,
                       nbins=caixas,
                       color_discrete_sequence= [cor],
                       labels = legenda,
                       width=largura,
                       height=altura)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    fig.update_layout(
                        xaxis_title=f"{nome_coluna}",
                        yaxis_title=f"{titulo_y}",
                    )
    fig.update_traces(opacity=0.75)
    
    return fig

def quant_dias(df):
    dias = df['CreationDate'].dt.strftime('%Y-%m-%d').unique()
    dias = len(dias)
    return dias

# Alltera o texto do status
def formata_status_media(value):
    return f"{value} ⬆️" if value == "Acima da Média" else f"{value} ⬇️"



def grafico_lb_combo(df, x_axis, yl, yb, x_name=None, y_name=None, titulo = None):
    fig = go.Figure()

    x = 3

    for lname, l in yl.items():
        fig.add_trace(go.Scatter(x=df[x_axis], y=df[l], mode='lines', name=lname, marker={'color': paleta_NMC[x]}))
        x+=1

    x = 0

    for bname, b in yb.items():
        fig.add_trace(go.Bar(x=df[x_axis], y=df[b], name=bname, marker={'color': paleta_NMC[x]}))
        x+=1


    fig.update_layout(title_text=titulo)
    fig.update_xaxes(title_text=x_name)
    fig.update_yaxes(title_text=y_name)

    return fig


### Função Tabela de Processos
def tabela_familias_processo(df1, df2):
    # Criando os dados agregados
    df = df1[['id','flow.name', 'nomeDoResponsavelDaFamilia','flowResult']].copy().drop_duplicates()
    df = df1.groupby(['id','flow.name','nomeDoResponsavelDaFamilia']).agg({'flowResult':'count'}).reset_index()
    
    df_ = df2.copy()

    df = df.merge(
        df_[['id', 'Status_Tarefa','Tasks.name']],
        how = 'left',
        on='id'
    )

    df = df[df['Status_Tarefa'] == 'Em andamento']

    df = df[['flowResult','flow.name','nomeDoResponsavelDaFamilia', 'Status_Tarefa', 'Tasks.name']].drop_duplicates()

    df = df.rename(columns={'Tasks.name':'Atividades','flowResult':'Quantidade', 'flow.name':'Ticket'})

    df['nomeDoResponsavelDaFamilia'] = df['nomeDoResponsavelDaFamilia'].str.title()

    return df

def plot_gantt(df, x_start, x_end, y, color, color_discrete_sequence, hover_name):
        fig = px.timeline(
                        df, 
                        x_start=x_start, 
                        x_end=x_end, 
                        y=y,
                        color=color,
                        color_discrete_sequence=color_discrete_sequence,
                        hover_name=hover_name
                        )

        fig.update_yaxes(autorange="reversed")          #if not specified as 'reversed', the tasks will be listed from bottom up       

        fig.update_layout(
                        title='Etapas do processo (Gantt)',
                        hoverlabel_bgcolor=roxo,   #Change the hover tooltip background color to a universal light blue color. If not specified, the background color will vary by team or completion pct, depending on what view the user chooses
                        bargap=0.2,
                        height=600,              
                        xaxis_title="", 
                        yaxis_title="",                   
                        title_x=0.5,                    #Make title centered                     
                        xaxis=dict(
                                tickfont_size=15,
                                tickangle = 0,
                                rangeslider_visible=True,
                                side ="top",            #Place the tick labels on the top of the chart
                                showgrid = True,
                                zeroline = True,
                                showline = True,
                                showticklabels = True,
                                tickformat="%x\n",      #Display the tick labels in certain format. To learn more about different formats, visit: https://github.com/d3/d3-format/blob/main/README.md#locale_format
                                )
                )
        
        return fig

