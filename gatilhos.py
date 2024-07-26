import streamlit as st
import pandas as pd
import card_models as cm
import setup
import okr_metrics
import funcoes_dashboard as fd 
import plotly.graph_objects as go
import datetime

# Cores NMC
roxo = "#521C78"
laranja = "#F0A800"
azul = "#121C4D"
azul_b = "#14A2dc"
vermelho = "#E8501C"
verde = "#198036"
amarelo = "#DDD326"
cinza = "#888DA6"
paleta_IVS = [azul_b, azul, amarelo, laranja, vermelho]
paleta_NMC = [roxo, laranja, azul, vermelho, azul_b, verde, amarelo]


def plot_line_chart(df, x_axis,y_axis):
    import plotly.express as px

    fig = px.line(df, x=x_axis, y=y_axis, text=y_axis, height=550)
    fig.update_traces(textposition="bottom right")
    fig.update_layout(yaxis_title="FATURAMENTO (R$)", xaxis_title="MESES", title='Histórico do Faturamento por contrato')

    st.plotly_chart(fig, use_container_width=True)

def criar_selectBox(lista, titulo='Selecione um ou mais index', select_text = 'Lista de index',
                    tipo = 'multiselect'):
    if tipo=='multiselect':
        selecao = st.multiselect(
            f'**{titulo}**',
            lista)

        change_text = f'''
                            <style>
                            .stMultiSelect div div div div div:nth-of-type(2) {{visibility: hidden;}}
                            .stMultiSelect div div div div div:nth-of-type(2)::before {{visibility: visible; content:"{select_text}"}}
                            div[data-baseweb="select"] > div {{
                            background-color: #A0A4B8;
                        }}
                            </style>
                            '''

        st.markdown(change_text, unsafe_allow_html=True)
    else:
        selecao = st.selectbox(
            f'**{titulo}**',
            lista)

        change_text = f'''
                            <style>
                            .stMultiSelect div div div div div:nth-of-type(2) {{visibility: hidden;}}
                            .stMultiSelect div div div div div:nth-of-type(2)::before {{visibility: visible; content:"{select_text}"}}
                            div[data-baseweb="select"] > div {{
                            background-color: #A0A4B8;
                        }}
                            </style>
                            '''

        st.markdown(change_text, unsafe_allow_html=True)
        
    return selecao

# @st.cache_data()
def criar_aba_faturamento(df, diretoria, dic_df, app='320'):
    # linha vazia
    df320_f = df.loc[df['Diretoria'].str.contains(diretoria + ' -')]
    df320_f.rename(columns={
        'contrato':'Contrato',
        'metaGeralFaturamento': 'Meta - Faturamento',
        'metaGeralLucroLiquido': 'Meta - Lucro líquido',
        'resultadoAlcancadoFaturamento': 'Resultado Alcançado - Faturamento',
        'PorcentagemAlcancadaFaturamento': 'Porcentagem Alcançado - Faturamento',
        'resultadoAlcancadoLucro': 'Resultado Alcançado - Lucro líquido',
        'PorcentagemAlcancadaLucro': 'Porcentagem Alcançado - Lucro líquido',
        'peso': 'Peso'
    }, inplace=True)
    cols = ['Contrato', 'Resultado Alcançado - Faturamento', 'Meta - Faturamento', 'Porcentagem Alcançado - Faturamento',
            'Resultado Alcançado - Lucro líquido', 'Meta - Lucro líquido', 'Porcentagem Alcançado - Lucro líquido']

    df320_f.fillna(0, inplace=True)

    
    #Adicionar gráfico e filtro do contrato
    col1, col2 = st.columns([1,1], gap='large')
    with col1:
        contratos_diretoria = dic_df[app][dic_df[app]['diretoria'].str.contains(diretoria + ' -')]['contrato'].unique()
        
        df_contrato_fat, df_contrato_luc, meta_lucro_mensal, meta_fat_freq_mensal = okr_metrics.get_metas_mes(df_app=dic_df[app],
                                                                                                             contrato=contratos_diretoria)
        
        fig = fd.px_bar_chart(df=df_contrato_fat,x_axis='periodoDeAvaliacaomoeda',
                                y_axis='resultadoAlcancadomoeda',texto=True, cor=roxo, altura=550)
            
        fig.update_layout(yaxis_title="FATURAMENTO (R$)", xaxis_title="MESES", title='Histórico do faturamento geral por mês')
        
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        select_contratos = criar_selectBox(lista = df320_f['Contrato'].unique(), titulo='Filtro por Contratos - Faturamento',
                                        select_text = 'Escolha uma ou mais opções', tipo = 'single_select')

        if dic_df[app][dic_df[app]['contrato']==select_contratos]['id'].empty:
            pass
        else:
            df_contrato_fat, df_contrato_luc, meta_lucro_mensal, meta_fat_freq_mensal = okr_metrics.get_metas_mes(df_app=dic_df[app], contrato=[select_contratos])
            
            
            fig = fd.px_bar_chart(df=df_contrato_fat,x_axis='periodoDeAvaliacaomoeda',
                                y_axis='resultadoAlcancadomoeda',texto=True, cor=roxo)
            
            fig.update_layout(yaxis_title="FATURAMENTO (R$)", xaxis_title="MESES", title='Histórico do faturamento do contrato')
            # Adicionar a linha da meta
            fig.add_trace(
                        go.Scatter(
                            x=df_contrato_fat['periodoDeAvaliacaomoeda'],
                            y=meta_fat_freq_mensal,
                            line=dict(color=azul_b),
                            name='Meta'
                        ))
            st.plotly_chart(fig, use_container_width=True)

# @st.cache_data()
def criar_aba_lucro(df, diretoria, dic_df, app='320'):
    # linha vazia
    df320_f = df.loc[df['Diretoria'].str.contains(diretoria + ' -')]
    df320_f.rename(columns={
        'contrato':'Contrato',
        'metaGeralFaturamento': 'Meta - Faturamento',
        'metaGeralLucroLiquido': 'Meta - Lucro líquido',
        'resultadoAlcancadoFaturamento': 'Resultado Alcançado - Faturamento',
        'PorcentagemAlcancadaFaturamento': 'Porcentagem Alcançado - Faturamento',
        'resultadoAlcancadoLucro': 'Resultado Alcançado - Lucro líquido',
        'PorcentagemAlcancadaLucro': 'Porcentagem Alcançado - Lucro líquido',
        'peso': 'Peso'
    }, inplace=True)
    cols = ['Contrato', 'Resultado Alcançado - Faturamento', 'Meta - Faturamento', 'Porcentagem Alcançado - Faturamento',
            'Resultado Alcançado - Lucro líquido', 'Meta - Lucro líquido', 'Porcentagem Alcançado - Lucro líquido']

    df320_f.fillna(0, inplace=True)
    
    #Adicionar gráfico e filtro do contrato
    col1, col2 = st.columns([1,1], gap='large')
    with col1:
        contratos_diretoria = dic_df[app][dic_df[app]['diretoria'].str.contains(diretoria + ' -')]['contrato'].unique()
        df_contrato_fat, df_contrato_luc, meta_lucro_mensal, meta_fat_freq_mensal = okr_metrics.get_metas_mes(df_app=dic_df[app], contrato=contratos_diretoria)
        
    
        
        fig = fd.px_bar_chart(df=df_contrato_luc,x_axis='periodoDeAvaliacaomoeda',
                                y_axis='resultadoAlcancadomoeda',texto=True, cor=roxo, altura=550)
            
        fig.update_layout(yaxis_title="LUCRO (R$)", xaxis_title="MESES", title='Histórico do lucro geral por mês')
        
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        
        select_contratos = criar_selectBox(lista = df320_f['Contrato'].unique(), titulo='Filtro por Contratos - Lucro',
                                        select_text = 'Escolha uma ou mais opções', tipo = 'single_select')

        if dic_df[app][dic_df[app]['contrato']==select_contratos]['id'].empty:
            pass
        else:
            df_contrato_fat, df_contrato_luc, meta_lucro_mensal, meta_fat_freq_mensal = okr_metrics.get_metas_mes(df_app=dic_df[app], contrato=[select_contratos])
            
            
            fig = fd.px_bar_chart(df=df_contrato_luc,x_axis='periodoDeAvaliacaomoeda',
                                y_axis='resultadoAlcancadomoeda',texto=True, cor=roxo)
            
            fig.update_layout(yaxis_title="LUCRO (R$)", xaxis_title="MESES", title='Histórico do lucro do contrato')
            # Adicionar a linha da meta
            fig.add_trace(
                        go.Scatter(
                            x=df_contrato_luc['periodoDeAvaliacaomoeda'],
                            y=meta_fat_freq_mensal,
                            line=dict(color=azul_b),
                            name='Meta'
                        ))
            st.plotly_chart(fig, use_container_width=True)

# @st.cache_data()
def criar_aba_vendas(dic_df, diretoria, app='315', tipo='VENDER'):
    import numpy as np
    import re
    # linha vazia
    df = dic_df[app].copy()
    id_ = df.loc[df['descricaoDaMetaMensal'].str.contains(tipo)]['id'].unique()
    df = df.loc[df['id'].isin(id_)]
    df_f = df.loc[df['diretoria'].str.contains(' - '+diretoria)]
    
        
    if diretoria == 'DCOM':
        df_ff = df[['diretoria', 'periodoDeAvaliacaomoeda','discriminacaoDoResultadoobservacoesmoeda', 'resultadoAlcancadomoeda', 'peso']].replace('NAN', np.nan)\
                                                                .dropna(subset = 'discriminacaoDoResultadoobservacoesmoeda')
 
        df_ff['Resultado Alcançado'] = df_ff['resultadoAlcancadomoeda']

        df_ff = df_ff.rename(columns = {
                'diretoria': 'Diretoria',
                'periodoDeAvaliacaomoeda': 'Periodicidade',
                'discriminacaoDoResultadoobservacoesmoeda': 'Discriminação da venda',
                'peso': 'Peso'
        })
        st.dataframe(df_ff[['Diretoria','Periodicidade','Discriminação da venda', 'Resultado Alcançado']], use_container_width=True)
        df_g = df_ff.groupby('Periodicidade')[['Resultado Alcançado']].sum()

        fig = fd.px_bar_chart(df=df_g.reset_index(),x_axis='Periodicidade',
                            y_axis='Resultado Alcançado',texto=True, cor=roxo, altura=550)
        
        fig.update_layout(yaxis_title="VALOR DA VENDA (R$)", xaxis_title="MESES", title='Histórico de vendas por mês')
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        df_f = df.loc[df['diretoria'].str.contains(' - '+diretoria)]
        df_ff = df_f[['diretoria', 'periodoDeAvaliacaomoeda','discriminacaoDoResultadoobservacoesmoeda', 'resultadoAlcancadomoeda', 'peso']].replace('NAN', np.nan).dropna(subset = 'discriminacaoDoResultadoobservacoesmoeda')
        l = []
        if df_ff['resultadoAlcancadomoeda'].empty:
            st.write('A diretoria ainda não realizou vendas')
        else:
            
            df_ff['Resultado Alcançado'] = df_ff['resultadoAlcancadomoeda']
            df_ff = df_ff.rename(columns = {
                    'discriminacaoDoResultadoobservacoesmoeda': 'Discriminação da venda',
                    'peso': 'Peso'
            })
            df_ff = df_ff.rename(columns = {
                            'diretoria': 'Diretoria',
                            'periodoDeAvaliacaomoeda': 'Periodicidade',
                            'discriminacaoDoResultadoobservacoesmoeda': 'Discriminação da venda',
                            'peso': 'Peso'
                    })

            st.dataframe(df_ff[['Diretoria','Periodicidade','Discriminação da venda', 'Resultado Alcançado']], use_container_width=True)
            df_g = df_ff.groupby('Periodicidade')[['Resultado Alcançado']].sum()

            fig = fd.px_bar_chart(df=df_g.reset_index(),x_axis='Periodicidade',
                                y_axis='Resultado Alcançado',texto=True, cor=roxo, altura=550)
            
            fig.update_layout(yaxis_title="VALOR DA VENDA (R$)", xaxis_title="MESES", title='Histórico de vendas por mês')
            
            st.plotly_chart(fig, use_container_width=True)
