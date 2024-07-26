import numpy as np
import streamlit as st
import pandas as pd
import card_models as cm
import setup
import okr_metrics
import datetime
import gatilhos
import math
import numpy as np
import funcoes_dashboard as fd 

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

# @st.cache_resource(show_spinner="Calculando...", ttl=datetime.timedelta(hours=1))
def pct_alcance_geral(df_outros, df320, diretoria=False):
    import numpy as np

    if diretoria!=False:
        df_outros = df_outros[df_outros['Diretoria'].str.contains(diretoria)]
        df320 = df320[df320['Diretoria'].str.contains(diretoria)]
        df320_f = df320.fillna(0)
        if df_outros.shape[0]==0 and df320_f.shape[0]==0:
            result = 0.0
            concluidos = 0.0
            n_concluidos = 0.0

        else:
            
            result = pd.concat([df_outros['Porcentagem Alcançada'], df320_f['PorcentagemAlcancadaFaturamento'], df320_f['PorcentagemAlcancadaLucro']]).to_frame()\
                                                                                        .replace(np.inf,np.nan)\
                                                                                        .dropna()
            result.columns = ['Porcentagem Alcançada']
            
            concluidos = result[result['Porcentagem Alcançada']>=100].shape[0]
            n_concluidos = result[result['Porcentagem Alcançada']<100].shape[0]
            pct = round(concluidos/(concluidos+n_concluidos)*100,2)
            return pct
    else:
        df320_f = df320.fillna(0)
        if df_outros.shape[0]==0 and df320_f.shape[0]==0:
            result = 0.0
            concluidos = 0.0
            n_concluidos = 0.0

        else:
            
            result = pd.concat([df_outros['Porcentagem Alcançada'], df320_f['PorcentagemAlcancadaFaturamento'], df320_f['PorcentagemAlcancadaLucro']]).to_frame()\
                                                                                        .replace(np.inf,np.nan)\
                                                                                        .dropna()
            result.columns = ['Porcentagem Alcançada']
            
            concluidos = result[result['Porcentagem Alcançada']>=100].shape[0]
            n_concluidos = result[result['Porcentagem Alcançada']<100].shape[0]
            pct = round(concluidos/(concluidos+n_concluidos)*100,2)
            return pct

def criar_selectBox(lista, titulo='Selecione um ou mais index', select_text = 'Lista de index'):
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
    return selecao

# @st.cache_resource(show_spinner="Calculando 315...", ttl=datetime.timedelta(hours=1))
def get_vendas(dic_df, df315, diretoria=False, app='315', tipo='VENDER'):
    import re
    # linha vazia
    if diretoria != False:
        df = dic_df[app].copy()
        df = df.loc[df['descricaoDaMetaMensal'].str.contains(tipo)]
        
        df315 = df315.loc[df315['metaIndividual'].str.contains(tipo)]
        df_f = df.loc[df['diretoria'].str.contains(' - '+diretoria)]
        if df_f.empty:
            return 0, 0
        else:
            
            resultado = round(float(df_f['totalAcumulado'].values[0]),0)
            pct = round((resultado/df315['Meta'].sum())*100,0)
            resultado = resultado/1000000
            
            return pct, resultado
    else:
        df = dic_df[app].replace('NAN', np.nan).dropna(subset = 'discriminacaoDoResultadoobservacoesmoeda')
        df = df.loc[df['descricaoDaMetaMensal'].str.contains(tipo, na=True)]

        
        df315 = df315.loc[df315['metaIndividual'].str.contains(tipo, na=True)]
        l = []

        resultado = df['totalAcumulado'].sum()
        pct = round((resultado/df315['Meta'].sum())*100,0)
        
        resultado = resultado/1000000
        return pct, resultado

def get_venda_gatilhos(dic_df, diretoria, app='315', tipo='VENDER'):

    # linha vazia
    df = dic_df[app].copy()
    id_ = df.loc[df['descricaoDaMetaMensal'].str.contains(tipo)]['id'].unique()
    df = df.loc[df['id'].isin(id_)]
    if diretoria == False:
        df = df
    else:
        df = df.loc[df['diretoria'].str.contains(' - ' + diretoria)]
    
    df_ff = df[['diretoria', 'periodoDeAvaliacaomoeda','discriminacaoDoResultadoobservacoesmoeda', 'resultadoAlcancadomoeda', 'peso']].replace('NAN', np.nan)\
                                                            .dropna(subset = 'discriminacaoDoResultadoobservacoesmoeda')

    df_ff['Resultado Alcançado'] = df_ff['resultadoAlcancadomoeda']

    df_ff = df_ff.rename(columns = {
            'diretoria': 'Diretoria',
            'periodoDeAvaliacaomoeda': 'Periodicidade',
            'discriminacaoDoResultadoobservacoesmoeda': 'Discriminação da venda',
            'peso': 'Peso'
    })
    # st.dataframe(df_ff[['Diretoria','Periodicidade','Discriminação da venda', 'Resultado Alcançado']], use_container_width=True)
    df_g = df_ff.groupby('Periodicidade')[['Resultado Alcançado']].sum()

    fig = fd.px_bar_chart(df=df_g.reset_index(),x_axis='Periodicidade',
                        y_axis='Resultado Alcançado',texto=True, cor=roxo, altura=550)
    
    fig.update_layout(yaxis_title="VALOR DA VENDA (R$)", xaxis_title="MESES", title='Histórico de vendas por mês')
    
    st.plotly_chart(fig, use_container_width=True)


def app(dic_df):
    icon_aluguel = 'fa-sharp fa-regular fa-handshake'
    icon_cedido = 'fa-solid fa-hand-holding-heart'
    icon_pessoas = 'fa-solid fa-people-group'
    icon_mulChef = 'fa-solid fa-venus'
    icon_cash = 'fa-solid fa-sack-dollar'
    icon_familia = 'fa-solid fa-people-roof'
    icon_house = 'fa-solid fa-house'
    icon_house_check = 'fa-solid fa-house-circle-check'
    icon_house_exclam = 'fa-solid fa-house-circle-exclamation'
    icon_ideniSim = 'fa-solid fa-hand-holding-dollar'
    icon_compAss = 'fa-solid fa-hands-holding-child'
    icon_sacoDin = 'fa-solid fa-sack-dollar'
    icon_ivsI = 'fa-solid fa-person-circle-exclamation'
    icon_ivsII = "fa-solid fa-person-rays"
    icon_shop = "fa-solid fa-store"

    cor_caixa1 = '#A88DBB'
    cor_caixa2 = '#7FC0A4'
    cor_caixa3 = '#7ED1EF'
    cor_caixa4 = laranja

    # customizar tabs
    css = '''
        <style>
            .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size:20px;
            }
        </style>
        '''
    st.markdown(css, unsafe_allow_html=True)

    col1, col2= st.columns([1.5, 2])

    
    # ----------- Pegar BDs --------------------------------------------------------------------------------------------------------
    df292, dic_metas = okr_metrics.get_df_metas(dic_df=dic_df, app='292')
    df292_dash = okr_metrics.df_to_dash(df292)
    df320 = okr_metrics.get_df_faturamento_lucro(dic_df=dic_df, app='320')
    df_g320, dic320 = okr_metrics.calcula_faturamento_lucro_por_diretoria(df320)
    df315, dic_metas315 = okr_metrics.get_df_metas(dic_df=dic_df, app='315')
    df_vendas, dic_vendas = okr_metrics.calcula_vendas_por_diretoria(df315)
    df_oturos = okr_metrics.format_outras_metas(df292, df315)
  
    # ------- Resultados chaves ---------------------------------------------------------------------------------------------------
    header_2 = ''f'<h1 style="color:{azul};font-size:34px;">Percentual de Alcance das metas</h1>'''
    st.markdown(header_2, unsafe_allow_html=True)
    st.write('Porcentagem geral das metas')

    # Metrica geral
    val = pct_alcance_geral(df_oturos,df320)
    pct_alcance = f'{val}%'
    cm.card_progress(val = val,val_meta=pct_alcance, titulo='Pecentual de Alcance',  icon='fa-solid fa-arrow-trend-up', cor=verde)
    
    # ------- Resultados chaves ---------------------------------------------------------------------------------------------------
    st.write('---')
    header_2 = ''f'<h1 style="color:{azul};font-size:34px;">Gatilhos de alta performance</h1>'''
    st.markdown(header_2, unsafe_allow_html=True)
    st.write("Os Quatro gatilhos são as metas (kR) mais importantes. ")
    
    c1, cint, c2 = st.columns([1,0.1,1])
    with c1:
        df315_venda = df315.loc[df315['metaIndividual'].str.contains('VENDER', na=True)]
        p_meta1 = round(((df315_venda['Resultado'].astype(float).sum()/1000000)/75)*100,2)
        meta1MM = round(df315_venda['Resultado'].astype(float).sum()/1000000,2).astype(str)+' MM'
       
        # ---- teste ----
        

        tab1, tab2 = st.tabs(['Card', 'Gráfico'])
        with tab1:
            cm.card_progress(val = p_meta1,val_meta=meta1MM, titulo='Crescer em todos mercados (vendas): META 75 MM',  icon='fa-solid fa-cart-plus', cor=azul)
        with tab2:
            get_venda_gatilhos(dic_df, diretoria=False, app='315', tipo='VENDER')

        tab1, tab2 = st.tabs(['Card', 'Gráfico'])
        with tab1:
            p_meta2 = int((df_g320['resultadoAlcancadoFaturamento'].sum()/(32*1000000))*100)
            meta2MM = (round(df_g320['resultadoAlcancadoFaturamento'].sum()/1000000,2)).astype(str)+' MM'
            cm.card_progress(val = p_meta2, val_meta=meta2MM, titulo='Faturamento: META 32 MM',  icon='fa-solid fa-sack-dollar', cor=azul)
        with tab2:
            contratos_diretoria = dic_df['320']['contrato'].unique()
            df_contrato_fat, df_contrato_luc, meta_lucro_mensal, meta_fat_freq_mensal = okr_metrics.get_metas_mes(df_app=dic_df['320'],
                                                                                                                contrato=contratos_diretoria)
            fig = fd.px_bar_chart(df=df_contrato_fat,x_axis='periodoDeAvaliacaomoeda',
                                y_axis='resultadoAlcancadomoeda',texto=True, cor=roxo, altura=550)
            
            fig.update_layout(yaxis_title="FATURAMENTO (R$)", xaxis_title="MESES", title='Histórico do faturamento geral por mês')
            
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        if df_g320['resultadoAlcancadoLucro'].sum()==0 and df_g320['resultadoAlcancadoFaturamento'].sum()==0:
            lucro_val = 0.0
            
        else:
            lucro_val = df_g320['resultadoAlcancadoLucro'].sum()/1000000
        
        tab1, tab2 = st.tabs(['Card', 'Gráfico'])
        with tab1:
            meta3MM = f'{(round(lucro_val,2))} MM'
            cm.card_progress(val = round((lucro_val/4.8)*100,1),val_meta=meta3MM, titulo='Lucro: Meta 4,8 MM equivalente a 15% do faturamento da empresa',  icon='fa-solid fa-piggy-bank', cor=azul)
        with tab2:
            contratos_diretoria = dic_df['320']['contrato'].unique()
            df_contrato_fat, df_contrato_luc, meta_lucro_mensal, meta_fat_freq_mensal = okr_metrics.get_metas_mes(df_app=dic_df['320'],
                                                                                                                contrato=contratos_diretoria)
            fig = fd.px_bar_chart(df=df_contrato_luc,x_axis='periodoDeAvaliacaomoeda',
                                y_axis='resultadoAlcancadomoeda',texto=True, cor=roxo, altura=550)
            
            fig.update_layout(yaxis_title="LUCRO (R$)", xaxis_title="MESES", title='Histórico do lucro geral por mês')
            
            st.plotly_chart(fig, use_container_width=True)
        p_meta4 = 'SIM'
        if p_meta4=='SIM':
            cm.card_info(icon='fa-solid fa-thumbs-up', cor=verde, valor=p_meta4, descricao='Manter Certificação do ESG')
        else:
            cm.card_info(icon='fa-solid fa-thumbs-down', cor=vermelho, valor=p_meta4, descricao='Manter Certificação do ESG')
            
    # linha vazia
    st.title('')

    # ------ DataFrame e Super metas -----------------------------------------------------------------------------------------
    st.write('---')
    header_2 = ''f'<h1 style="color:{azul};font-size:34px;">Resultados das Diretorias</h1>'''
    st.markdown(header_2, unsafe_allow_html=True)
    st.write('*Visão geral das Diretorias*')

    # if st.button("👉 Página das Diretorias"):
    #     st.switch_page("./pages/pg_okr_diretoria.py")

    with st.container(border=True):
        tab_geral1, tab_fat1, tab_luc1, tab_vendas1 = st.tabs(['Geral', 'Faturamento', 'Lucro', 'Vendas'])
        
        with tab_geral1:
            st.title('DDIAT')
            st.write('*Diretoria Deslocamento Involuntário e Análise territorial*')
            c_1, c_2, c_3 = st.columns([0.1,1,1.5])
            with c_1:
                st.markdown('<p style="font-size 3px">Geral</p>', unsafe_allow_html=True)
            with c_2:
                val = pct_alcance_geral(df_oturos,df320, diretoria='DDIAT')
                cm.progress_bar(val=val, cor=azul_b)
            pct3, val3 = get_vendas(dic_df=dic_df, df315=df315, diretoria='DDIAT', app='315')
            if math.isnan(val3):
                val3=0
                pct3=0
            cm.progressBarCircle(val1=dic320['DDIAT'][0], val2=dic320['DDIAT'][1], val3=f'{round(val3,2)} MM',pct1=dic320['DDIAT'][2], pct2=dic320['DDIAT'][3], pct3=pct3, texto1='Faturamento',
                                texto2='Lucro',texto3='Vendas', cor1=azul_b, cor2=laranja, cor3=roxo)
        with tab_fat1:
            st.title('DDIAT')
            gatilhos.criar_aba_faturamento(df=df320, diretoria='DDIAT', dic_df=dic_df, app='320')
        with tab_luc1:
            st.title('DDIAT')
            gatilhos.criar_aba_lucro(df=df320, diretoria='DDIAT', dic_df=dic_df, app='320')
        with tab_vendas1:
            st.title('DDIAT')
            gatilhos.criar_aba_vendas(diretoria='DDIAT', dic_df=dic_df, app='315', tipo='VENDER')


    with st.container(border=True):
        #Deixar só vendas
        
        tab_geral2, tab_vendas2, tab_prospeccao= st.tabs(['Geral', 'Vendas', 'Prospecção de venda'])
        with tab_geral2:
            st.title('DCOM')
            st.write('*Diretoria Comercial*')
            c_1, c_2, c_3 = st.columns([0.1,1,1.5])
            with c_1:
                st.markdown('<p style="font-size 3px">Geral</p>', unsafe_allow_html=True)
            with c_2:
                df_geral = pd.concat([df292, df315, df320])
                df_ = okr_metrics.formata_df_geral(df_=df_geral, diretoria = 'DCOM')
                concluidos = df_[df_['Porcentagem Alcançada']>=100].shape[0]
                n_concluidos = df_[df_['Porcentagem Alcançada']<100].shape[0]
                val = round(concluidos/(concluidos+n_concluidos)*100,2)
                cm.progress_bar(val=val, cor=azul_b)
            pct3, val3 = get_vendas(dic_df=dic_df, df315=df315,diretoria=False, app='315', tipo='VENDER')
            pct2, val2 = get_vendas(dic_df=dic_df, df315=df315,diretoria=False, app='315', tipo='PROSPECTAR') 
            if math.isnan(val3):
                val3=0
                pct3=0
            cm.progressBarCircle2(val1='0 MM', val2=f'{round(val2,2)} MM', val3=f'{round(val3,2)} MM', pct1=0, pct2=pct2,pct3=pct3, texto1='Faturamento',
                                texto2='Prospecção',texto3='Vendas', cor1=azul_b, cor2=laranja, cor3=roxo)
        with tab_vendas2:
            st.title('DCOM')
            gatilhos.criar_aba_vendas(diretoria='DCOM', dic_df=dic_df, app='315', tipo='VENDER')
        with tab_prospeccao:
            st.title('DCOM')
            gatilhos.criar_aba_vendas(diretoria='DCOM', dic_df=dic_df, app='315', tipo='PROSPECTAR')
        
    
    with st.container(border=True):
        tab_geral3, tab_fat3, tab_luc3, tab_vendas3 = st.tabs(['Geral', 'Faturamento', 'Lucro', 'Vendas'])
        with tab_geral3:
            st.title('DES')
            st.write('*Diretoria de SocioEconomia e Engajamento*')
            c_1, c_2, c_3 = st.columns([0.1,1,1.5])
            with c_1:
                st.markdown('<p style="font-size 3px">Geral</p>', unsafe_allow_html=True)
            with c_2:
                val = pct_alcance_geral(df_oturos,df320, diretoria='DES')
                cm.progress_bar(val=val, cor=azul_b)
            pct3, val3 = get_vendas(dic_df=dic_df, df315=df315,diretoria='DES', app='315')

            if math.isnan(val3):
                val3=0
                pct3=0
            cm.progressBarCircle(dic320['DES'][0], val2=dic320['DES'][1], val3=f'{val3} MM',pct1=dic320['DES'][2], pct2=dic320['DES'][3],pct3=pct3, texto1='Faturamento',
                        texto2='Lucro',texto3='Vendas', cor1=azul_b, cor2=laranja, cor3=roxo)

        with tab_fat3:
            st.title('DES')
            gatilhos.criar_aba_faturamento(df=df320, diretoria='DES', dic_df=dic_df, app='320')
        with tab_luc3:
            st.title('DES')
            gatilhos.criar_aba_lucro(df=df320, diretoria='DES', dic_df=dic_df, app='320')
        with tab_vendas3:
            st.title('DES')
            gatilhos.criar_aba_vendas(diretoria='DES', dic_df=dic_df, app='315')



    with st.container(border=True):
        tab_geral4, tab_fat4, tab_luc4, tab_vendas4 = st.tabs(['Geral', 'Faturamento', 'Lucro', 'Vendas'])
        with tab_geral4:
            st.title('DASA')
            st.write('*Diretoria de Desenv. Ambiental, Saneamento e Agroeco.*')
            c_1, c_2, c_3 = st.columns([0.1,1,1.5])
            with c_1:
                st.markdown('<p style="font-size 3px">Geral</p>', unsafe_allow_html=True)
            with c_2:
                val = pct_alcance_geral(df_oturos,df320, diretoria='DASA')
                cm.progress_bar(val=val, cor=azul_b)
            pct3, val3 = get_vendas(dic_df=dic_df, df315=df315,diretoria='DASA', app='315')
            if math.isnan(val3):
                val3=0
                pct3=0
            cm.progressBarCircle(val1=dic320['DASA'][0], val2=dic320['DASA'][1], val3=f'{round(val3,2)} MM',pct1=dic320['DASA'][2], pct2=dic320['DASA'][3], pct3=pct3, texto1='Faturamento',
                                texto2='Lucro',texto3='Vendas', cor1=azul_b, cor2=laranja, cor3=roxo)
        
        with tab_fat4:
            st.title('DASA')
            gatilhos.criar_aba_faturamento(df=df320, diretoria='DASA', dic_df=dic_df, app='320')
        with tab_luc4:
            st.title('DASA')
            gatilhos.criar_aba_lucro(df=df320, diretoria='DASA', dic_df=dic_df, app='320')
        with tab_vendas4:
            st.title('DASA')
            gatilhos.criar_aba_vendas(diretoria='DASA', dic_df=dic_df, app='315')


    with st.container(border=True):
        tab_geral4, tab_fat4, tab_luc4, tab_vendas4 = st.tabs(['Geral', 'Faturamento', 'Lucro', 'Vendas'])
        with tab_geral4:
            st.title('GAGR')
            st.write('*Gerência de Agronegócios - GAGR*')
            c_1, c_2, c_3 = st.columns([0.1,1,1.5])
            with c_1:
                st.markdown('<p style="font-size 3px">Geral</p>', unsafe_allow_html=True)
            with c_2:
                val = pct_alcance_geral(df_oturos,df320, diretoria='GAGR')
                cm.progress_bar(val=val, cor=azul_b)
            pct3, val3 = get_vendas(dic_df=dic_df, df315=df315,diretoria='GAGR', app='315')
            if math.isnan(val3):
                val3=0
                pct3=0
            cm.progressBarCircle(val1=dic320['GAGR'][0], val2=dic320['GAGR'][1], val3=f'{round(val3,2)} MM',pct1=dic320['GAGR'][2], pct2=dic320['GAGR'][3], pct3=pct3, texto1='Faturamento',
                                texto2='Lucro',texto3='Vendas', cor1=azul_b, cor2=laranja, cor3=roxo)
        
        with tab_fat4:
            st.title('GAGR')
            gatilhos.criar_aba_faturamento(df=df320, diretoria='GAGR', dic_df=dic_df, app='320')
        with tab_luc4:
            st.title('GAGR')
            gatilhos.criar_aba_lucro(df=df320, diretoria='GAGR', dic_df=dic_df, app='320')
        with tab_vendas4:
            st.title('GAGR')
            gatilhos.criar_aba_vendas(diretoria='GAGR', dic_df=dic_df, app='315')

    with st.container(border=True):
        tab_geral5, tab_fat5, tab_luc5, tab_vendas5 = st.tabs(['Geral', 'Faturamento', 'Lucro', 'Vendas'])
        with tab_geral5:
            st.title('DPUB')
            st.write('*Diretoria de Negócios Públicos*')
            c_1, c_2, c_3 = st.columns([0.1,1,1.5])
            with c_1:
                st.markdown('<p style="font-size 3px">Geral</p>', unsafe_allow_html=True)
            with c_2:
                val = pct_alcance_geral(df_oturos,df320, diretoria='DPUB')
                cm.progress_bar(val=val, cor=azul_b)
            try:
                 pct3, val3 = get_vendas(dic_df=dic_df, df315=df315,diretoria='DPUB', app='315')
            except:
                val3=0
                pct3=0
            if math.isnan(val3):
                val3=0
                pct3=0

            cm.progressBarCircle(val1=dic320['DPUB'][0], val2=dic320['DPUB'][1], val3=f'{round(val3,2)} MM',pct1=dic320['DPUB'][2], pct2=dic320['DPUB'][3],pct3=pct3, texto1='Faturamento',
                                texto2='Lucro',texto3='Vendas', cor1=azul_b, cor2=laranja, cor3=roxo)
        with tab_fat5:
            st.title('DPUB')
            gatilhos.criar_aba_faturamento(df=df320, diretoria='DPUB', dic_df=dic_df, app='320')
        with tab_luc5:
            st.title('DPUB')
            gatilhos.criar_aba_lucro(df=df320, diretoria='DPUB', dic_df=dic_df, app='320')
        with tab_vendas5:
            st.title('DPUB')
            gatilhos.criar_aba_vendas(diretoria='DPUB', dic_df=dic_df, app='315')

    
    with st.container(border=True):
        tab_geral5, tab_fat5, tab_luc5, tab_vendas5 = st.tabs(['Geral', 'Faturamento', 'Lucro', 'Vendas'])
        with tab_geral5:
            st.title('DRF')
            st.write('*Diretoria de Negócios Públicos*')
            c_1, c_2, c_3 = st.columns([0.1,1,1.5])
            with c_1:
                st.markdown('<p style="font-size 3px">Geral</p>', unsafe_allow_html=True)
            with c_2:
                val = pct_alcance_geral(df_oturos,df320, diretoria='DRF')
                cm.progress_bar(val=val, cor=azul_b)
            try:
                 pct3, val3 = get_vendas(dic_df=dic_df, df315=df315,diretoria='DRF', app='315')
            except:
                val3=0
                pct3=0
            if math.isnan(val3):
                val3=0
                pct3=0

            cm.progressBarCircle(val1=dic320['DRF'][0], val2=dic320['DRF'][1], val3=f'{round(val3,2)} MM',pct1=dic320['DRF'][2], pct2=dic320['DRF'][3],
                                 pct3=pct3, texto1='Faturamento',
                                texto2='Lucro',texto3='Vendas', cor1=azul_b, cor2=laranja, cor3=roxo)
        with tab_fat5:
            st.title('DRF')
            gatilhos.criar_aba_faturamento(df=df320, diretoria='DRF', dic_df=dic_df, app='320')
        with tab_luc5:
            st.title('DRF')
            gatilhos.criar_aba_lucro(df=df320, diretoria='DRF', dic_df=dic_df, app='320')
        with tab_vendas5:
            st.title('DRF')
            gatilhos.criar_aba_vendas(diretoria='DRF', dic_df=dic_df, app='315')
    