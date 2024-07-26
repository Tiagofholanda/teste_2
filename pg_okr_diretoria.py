import streamlit as st
import pandas as pd
import card_models as cm
import setup
import okr_metrics
import funcoes_dashboard as fd 
import plotly.graph_objects as go
import datetime
from streamlit_dynamic_filters import DynamicFilters
import numpy as np
import re
import gatilhos

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

@st.cache_resource(show_spinner="Calculando...", ttl=datetime.timedelta(hours=1))
def pct_alcance_geral(df_outros,df320):
    import numpy as np
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

@st.cache_resource(show_spinner="Calculando...", ttl=datetime.timedelta(hours=1))
def metas_concluidas(df_outros, df320):
        import numpy as np
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
        return concluidos, n_concluidos

@st.cache_resource(show_spinner="Calculando...", ttl=datetime.timedelta(hours=1))
def metas_concluidas_colaborador(df):
        df320_f = df.fillna(0)
        if df320_f.shape[0]==0:
            concluidos = 0.0
            n_concluidos = 0.0

        else:
            concluidos = df320_f[df320_f['Porcentagem Alcançada']>=100].shape[0]
            n_concluidos = df320_f[df320_f['Porcentagem Alcançada']<100].shape[0]
        
        return concluidos, n_concluidos

def criar_selectBox(lista, titulo='Selecione um ou mais index', select_text = 'Lista de index',
                    tipo = 'multiselect', all_values = False):
    if tipo=='multiselect':
        if all_values != False:
            selecao = st.multiselect(
            f'**{titulo}**',
            lista,lista)

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

@st.cache_resource(show_spinner="Calculando 315...", ttl=datetime.timedelta(hours=1))
def get_vendas(dic_df, diretoria, app='315'):
    # linha vazia
    df = dic_df[app]
    df_f = df.loc[df['diretoria'].str.contains(' - '+diretoria)]
    return df_f['totalAcumulado'].sum()

def app(dic_df, tipo_acesso):
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
    # ----------- Pegar BDs --------------------------------------------------------------------------------------------------------
    df292, dic_metas = okr_metrics.get_df_metas(dic_df=dic_df, app='292')
    df292_dash = okr_metrics.df_to_dash(df292)
    df320 = okr_metrics.get_df_faturamento_lucro(dic_df=dic_df, app='320')
    df315, dic_metas315 = okr_metrics.get_df_metas(dic_df=dic_df, app='315')
    df_geral = pd.concat([df292, df315, df320])
    # 'periodo', 'frequenciaDeMensuracao'

    col1,colint, col2= st.columns([1,0.2, 1], gap='large')
    with col1:
        diretorias = tipo_acesso
        selecao = st.selectbox(
                            "**Diretoria**",
                            diretorias,
                            placeholder="Escolha uma opção...",
                            )
    if selecao == None:
        nome_diretoria = ''
        pass
    else:
        nome_diretoria = selecao
        n = nome_diretoria.split('- ')
    # Fitrar BD
    
    if n[1] == 'DAF':
        df320_f = df320.copy()
        df292_f = df292.loc[df292['Diretoria'].str.contains(' - '+n[1])]
        df315_f = df315.loc[df315['Diretoria'].str.contains(' - '+n[1])]
    elif n[1] == 'DCOM':
        df320_f = df320.loc[df320['Diretoria'].str.contains(n[1]+' -')]
        df292_f = df292.loc[df292['Diretoria'].str.contains(' - '+n[1])]
        df315_f = df315.copy()
    else:
        df320_f = df320.loc[df320['Diretoria'].str.contains(n[1]+' -')]
        df292_f = df292.loc[df292['Diretoria'].str.contains(' - '+n[1])]
        df315_f = df315.loc[df315['Diretoria'].str.contains(' - '+n[1])]
        
    df_g320 = okr_metrics.calcula_faturamento_lucro_por_diretoria(df320_f, exportar_dic=False)
    df_outros = okr_metrics.format_outras_metas(df292_f, df315_f)
    # ------- Resultados Geral ---------------------------------------------------------------------------------------------------
    
    header_2 = ''f'<h1 style="color:{azul};font-size:34px;">Resultado - {n[1]}</h1>'''
    st.markdown(header_2, unsafe_allow_html=True)


    # Metrica geral
    if n[1] == 'DCOM':
        c1, cint, c2 = st.columns([1,0.1,0.8])
        with c1:
            df_ = okr_metrics.formata_df_geral(df_=df_geral, diretoria = n[1])
            concluidos = df_[df_['Porcentagem Alcançada']>=100].shape[0]
            n_concluidos = df_[df_['Porcentagem Alcançada']<100].shape[0]
            pct = round(concluidos/(concluidos+n_concluidos)*100,2)
            tab1, tab2 = st.tabs(['Card', ' '])
            with tab1:
                val = pct_alcance_geral(df_outros, df320_f)
                pct_alcance = f'{pct}%'
                cm.card_progress(val = pct,val_meta=pct_alcance, titulo='Pecentual de Alcance',
                                icon='fa-solid fa-arrow-trend-up', cor=verde)
            
        with c2: 
            df_ = okr_metrics.formata_df_geral(df_=df_geral, diretoria = n[1])
            concluidos = df_[df_['Porcentagem Alcançada']>=100].shape[0]
            n_concluidos = df_[df_['Porcentagem Alcançada']<100].shape[0]
            
            tab1, tab2 = st.tabs(['Card', 'Gráfico'])
            with tab1:
                metas_bat = concluidos
                metas_n_bat = n_concluidos
                cm.card_info(icon='fa-solid fa-arrows-down-to-people', cor=azul, valor=f'{metas_bat}/{metas_n_bat}',
                            descricao='Metas concluídas x Em andamento<p style="font-size:360%;"> </p>')
            with tab2:
                okr_metrics.ploty_bar(y=[metas_bat,metas_n_bat])
    else:
        c1, cint, c2 = st.columns([1,0.1,0.8])
        with c1:
            tab1, tab2 = st.tabs(['Card', ' '])
            with tab1:
                val = pct_alcance_geral(df_outros, df320_f)
                pct_alcance = f'{val}%'
                cm.card_progress(val = val,val_meta=pct_alcance, titulo='Pecentual de Alcance',
                                icon='fa-solid fa-arrow-trend-up', cor=verde)
            
        with c2:
            df_metas_concluidas = metas_concluidas(df_outros, df320_f)
            concluidos, n_concluidos = df_metas_concluidas
            tab1, tab2 = st.tabs(['Card', 'Gráfico'])
            with tab1:
                metas_bat = concluidos
                metas_n_bat = n_concluidos
                cm.card_info(icon='fa-solid fa-arrows-down-to-people', cor=azul, valor=f'{metas_bat}/{metas_n_bat}',
                            descricao='Metas concluídas x Em andamento<p style="font-size:360%;"> </p>')
            with tab2:
                okr_metrics.ploty_bar(y=[metas_bat,metas_n_bat])


    # Trazer gatilhos de alta performance do okr geral
    # ------- Resultados chaves ---------------------------------------------------------------------------------------------------
    st.write('---')
    header_2 = ''f'<h1 style="color:{azul};font-size:34px;">Gatilhos de alta performance - {n[1]}</h1>'''
    st.markdown(header_2, unsafe_allow_html=True)

    st.write("Os Quatro gatilhos são as metas (kR) mais importantes. ")

    # Gatilhos  
    vendas = setup.gatilhos_diretorias[n[-1]][0]
    faturamento = setup.gatilhos_diretorias[n[-1]][1]
    lucroLiquido = setup.gatilhos_diretorias[n[-1]][2]
    try:
        vendas_val = float(re.findall("\d+\.\d+", vendas.replace(',', '.'))[0])
    except:
        vendas_val = float(re.findall("\d+", vendas)[0])

    try:
        faturamento_val = float(re.findall("\d+\.\d+", faturamento.replace(',', '.'))[0])
    except:
        faturamento_val = float(re.findall("\d+", faturamento)[0])

    

    if n[1] == 'DAF':
        c1, cint, c2 = st.columns([1,0.1,1])
        with c1:
            
            p_meta2 = int((df_g320['resultadoAlcancadoFaturamento'].sum()/(faturamento_val*1000000))*100)
            meta2MM = (round(df_g320['resultadoAlcancadoFaturamento'].sum()/1000000,2)).astype(str)+' MM'
            cm.card_progress(val = p_meta2, val_meta=meta2MM, titulo=f'Faturamento: META {faturamento}',  icon='fa-solid fa-sack-dollar', cor=azul)
            p_meta4 = 'SIM'
            if p_meta4=='SIM':
                cm.card_info(icon='fa-solid fa-thumbs-up', cor=verde, valor=p_meta4, descricao='Manter Certificação do ESG')
            else:
                cm.card_info(icon='fa-solid fa-thumbs-down', cor=vermelho, valor=p_meta4, descricao='Manter Certificação do ESG')
        with c2:     
            if df_g320['resultadoAlcancadoLucro'].sum()==0 and df_g320['resultadoAlcancadoFaturamento'].sum()==0:
                lucro_val = 0.0
                
            else:
                lucro_val = df_g320['resultadoAlcancadoLucro'].sum()/1000000
            
            meta3MM = f'{(round(lucro_val,2))} MM'
            
            try:
                lucro = float(re.findall("\d+\.\d+", lucroLiquido.replace(',', '.'))[0])
            except:
                lucro = float(re.findall("\d+", lucroLiquido)[0])
            cm.card_progress(val = round((lucro_val/lucro)*100,1),val_meta=meta3MM, titulo=f'Lucro: META {lucroLiquido} MM',  icon='fa-solid fa-piggy-bank', cor=azul)
            
        
    elif n[1] == 'DCOM':
        c1, cint, c2 = st.columns([1,0.1,1])
        with c1:
            df_prospec = dic_df['315'].copy()
            id_ = df_prospec.loc[df_prospec['metaIndividual'].str.contains('VENDER')]['id']
            df315_f = df_prospec.loc[df_prospec['id'].isin(id_)]
            p_meta1 = round(((df315_f['totalAcumulado'].astype(float).sum()/1000000)/75)*100,2)
            meta1MM = round(df315_f['totalAcumulado'].astype(float).sum()/1000000,2).astype(str)+' MM'
            cm.card_progress(val = p_meta1,val_meta=meta1MM, titulo=f'Crescer em todos mercados (vendas): META {vendas} MM',  icon='fa-solid fa-cart-plus', cor=azul)
        with c2:
            df_prospec = dic_df['315'].copy()
            id_ = df_prospec.loc[df_prospec['metaIndividual'].str.contains('PROSPECTAR')]['id']
            df315_f = df_prospec.loc[df_prospec['id'].isin(id_)]
            p_meta1 = round(((df315_f['totalAcumulado'].astype(float).sum()/1000000)/500)*100,2)
            meta1MM = round(df315_f['totalAcumulado'].astype(float).sum()/1000000,2).astype(str)+' MM'
            cm.card_progress(val = p_meta1,val_meta=meta1MM, titulo=f'Prospecção de vendas: META 500 MM',  icon='fa-solid fa-cart-plus', cor=azul)
            
         
    else:
        c1, cint, c2 = st.columns([1,0.1,1])
        with c1:
            df315_f = df315_f.loc[df315_f['metaIndividual'].str.contains('VENDER')]
            p_meta1 = round(((df315_f['Resultado'].astype(float).sum()/1000000)/vendas_val)*100,2)
            meta1MM = round(df315_f['Resultado'].astype(float).sum()/1000000,2).astype(str)+' MM'
            cm.card_progress(val = p_meta1,val_meta=meta1MM, titulo=f'Crescer em todos mercados (vendas): META {vendas}',  icon='fa-solid fa-cart-plus', cor=azul)


            # Verificar se faturamento_val não é zero para evitar divisão por zero
            if faturamento_val != 0:
             p_meta2 = int((df_g320['resultadoAlcancadoFaturamento'].sum() / (faturamento_val * 1000000)) * 100)
            else:
             p_meta2 = 0  # Ou outro valor apropriado, dependendo do contexto

            # Calcula o valor total alcançado em milhões e converte para string
            meta2MM = str(round(df_g320['resultadoAlcancadoFaturamento'].sum() / 1000000, 2)) + ' MM'
            
            p_meta2 = int((df_g320['resultadoAlcancadoFaturamento'].sum()/(faturamento_val*1000000))*100)
            meta2MM = (round(df_g320['resultadoAlcancadoFaturamento'].sum()/1000000,2)).astype(str)+' MM'

            cm.card_progress(val = p_meta2, val_meta=meta2MM, titulo=f'Faturamento: META {faturamento}',  icon='fa-solid fa-sack-dollar', cor=azul)
        with c2:    
            
            if df_g320['resultadoAlcancadoLucro'].sum()==0 and df_g320['resultadoAlcancadoFaturamento'].sum()==0:
                lucro_val = 0.0
                
            else:
                lucro_val = df_g320['resultadoAlcancadoLucro'].sum()/1000000
            meta3MM = f'{(round(lucro_val,2))} MM'
            try:
                lucro = float(re.findall("\d+\.\d+", lucroLiquido.replace(',', '.'))[0])
            except:
                lucro = float(re.findall("\d+", lucroLiquido)[0])
            cm.card_progress(val = round((lucro_val/lucro)*100,1),val_meta=meta3MM, titulo=f'Lucro: META {lucroLiquido} MM',  icon='fa-solid fa-piggy-bank', cor=azul)
        

    st.title('')
    st.write('---')

    # Detalhamento das metas -----------------------------------------------------------
    header_2 = ''f'<h1 style="color:{azul};font-size:34px;">Metas - {n[1]}</h1>'''
    st.markdown(header_2, unsafe_allow_html=True)

    if n[1] == 'DCOM':
        # ----- Metas OKR 1-2-3-4 ---------------------------------------------------------------
        tab1, tab2, tab3 = st.tabs(['Detalhamento das metas', 'Vendas', 'Prospecção de venda'])
        with tab1:
            st.title('Tabela')
            df_ = okr_metrics.formata_df_geral(df_=df_geral, diretoria = n[1])

            dynamic_filters = DynamicFilters(df_, 
                                            filters=['OKR','KR', 'Meta Individual', 'Nivel de Desdobramento', 'Colaborador'])

            dynamic_filters.display_filters(location='columns', num_columns=2, gap='large')

            # dynamic_filters.display_df()
            df_filtered = dynamic_filters.filter_df()

            
            st.write('---')
            # Se precisar filtrar as colunas da tabela colocar aqui
            
            colunas_tabela = ['OKR','KR','Nivel de Desdobramento','Colaborador','Diretorias que participam','Meta Individual',
                            'Tipo de medida','Periodo','Frequência de Mensuração', 'Meta', 'Resultado', 'Porcentagem Alcançada']

            st.dataframe(df_filtered[colunas_tabela].sort_values('Porcentagem Alcançada', ascending=False), use_container_width=True, hide_index=True,
                            column_config={
                                            "Porcentagem Alcançada": st.column_config.ProgressColumn(
                                                                                                    "Porcentagem Alcançada",
                                                                                                    help="Percentual alcançado das metas",
                                                                                                    format="%.0f%%",
                                                                                                    min_value=0,
                                                                                                    max_value=100,
                                                                                                ),
                                            },
                            )
        
            
            # configurar altura da barra
            if df_filtered.shape[0]<=5:
                altura=200
            elif df_filtered.shape[0]>5 and df_filtered.shape[0]<=10:
                altura=400
            elif df_filtered.shape[0]>10 and df_filtered.shape[0]<=15:
                altura=600
            elif df_filtered.shape[0]>15 and df_filtered.shape[0]<=20:
                altura=850
            elif df_filtered.shape[0]>20 and df_filtered.shape[0]<=40:
                altura=900  
            elif df_filtered.shape[0]>40 and df_filtered.shape[0]<=1000:
                altura=1600  

            fig = fd.px_bar_chart(df=df_filtered,x_axis='Porcentagem Alcançada',
                                    y_axis='Meta Individual',texto=True, cor=azul_b,orientacao='h', altura=altura)
            fig.update_layout(yaxis_title="", xaxis_title="(%)", title='Metas')
            # Adicionar a linha da meta
            fig.add_vline(x=100, line_width=5, line_dash="dash", line_color=laranja,
                            annotation_text="100%",
                            annotation_font_size=20,
                            annotation_position="top")
            st.plotly_chart(fig, use_container_width=True)
            

        # ---- TABELA ----------------------------------
        with tab2:
            gatilhos.criar_aba_vendas(diretoria='DCOM', dic_df=dic_df, app='315', tipo='VENDER')
        with tab3:
            gatilhos.criar_aba_vendas(diretoria='DCOM', dic_df=dic_df, app='315', tipo='PROSPECTAR')
           
    else:
        # ----- Metas OKR 1-2-3-4 ---------------------------------------------------------------
        tab1, tab2 = st.tabs(['Detalhamento das metas', 'Contratos'])
        with tab1:
            st.title('Tabela')
            if n[1] == 'DCOM':
                df_ = okr_metrics.formata_df_geral(df_=df_geral, diretoria = n[1])
            else:
                df_ = df_outros.copy()

            dynamic_filters = DynamicFilters(df_, 
                                            filters=['OKR','KR', 'Meta Individual', 'Nivel de Desdobramento', 'Colaborador'])

            dynamic_filters.display_filters(location='columns', num_columns=2, gap='large')

            # dynamic_filters.display_df()
            df_filtered = dynamic_filters.filter_df()

            
            st.write('---')
            # Se precisar filtrar as colunas da tabela colocar aqui
            
            colunas_tabela = ['OKR','KR','Nivel de Desdobramento','Colaborador','Diretorias que participam','Meta Individual',
                            'Tipo de medida','Periodo','Frequência de Mensuração', 'Meta', 'Resultado', 'Porcentagem Alcançada']

            st.dataframe(df_filtered[colunas_tabela].sort_values('Porcentagem Alcançada', ascending=False), use_container_width=True, hide_index=True,
                            column_config={
                                            "Porcentagem Alcançada": st.column_config.ProgressColumn(
                                                                                                    "Porcentagem Alcançada",
                                                                                                    help="Percentual alcançado das metas",
                                                                                                    format="%.0f%%",
                                                                                                    min_value=0,
                                                                                                    max_value=100,
                                                                                                ),
                                            },
                            )
        
            
            # configurar altura da barra
            if df_filtered.shape[0]<=5:
                altura=200
            elif df_filtered.shape[0]>5 and df_filtered.shape[0]<=10:
                altura=400
            elif df_filtered.shape[0]>10 and df_filtered.shape[0]<=15:
                altura=600
            elif df_filtered.shape[0]>15 and df_filtered.shape[0]<=20:
                altura=850
            elif df_filtered.shape[0]>20 and df_filtered.shape[0]<=40:
                altura=900  
            elif df_filtered.shape[0]>40 and df_filtered.shape[0]<=1000:
                altura=1600  

            fig = fd.px_bar_chart(df=df_filtered,x_axis='Porcentagem Alcançada',
                                    y_axis='Meta Individual',texto=True, cor=azul_b,orientacao='h', altura=altura)
            fig.update_layout(yaxis_title="", xaxis_title="(%)", title='Metas')
            # Adicionar a linha da meta
            fig.add_vline(x=100, line_width=5, line_dash="dash", line_color=laranja,
                            annotation_text="100%",
                            annotation_font_size=20,
                            annotation_position="top")
            st.plotly_chart(fig, use_container_width=True)
            

        # ---- TABELA ----------------------------------
        with tab2:
            # linha vazia
            st.title('Tabela')
            df320_f.rename(columns={
                'contrato':'Contrato',
                'metaGeralFaturamento': 'Meta - Fatuamento',
                'metaGeralLucroLiquido': 'Meta - Lucro líquido',
                'resultadoAlcancadoFaturamento': 'Resultado Alcançado - Faturamento',
                'PorcentagemAlcancadaFaturamento': 'Porcentagem Alcançado - Faturamento',
                'resultadoAlcancadoLucro': 'Resultado Alcançado - Lucro líquido',
                'PorcentagemAlcancadaLucro': 'Porcentagem Alcançado - Lucro líquido',
                'peso': 'Peso'
            }, inplace=True)
            cols = ['Contrato', 'Resultado Alcançado - Faturamento', 'Meta - Fatuamento', 'Porcentagem Alcançado - Faturamento',
                    'Resultado Alcançado - Lucro líquido', 'Meta - Lucro líquido', 'Porcentagem Alcançado - Lucro líquido']

            df320_f.fillna(0, inplace=True)
            st.dataframe(df320_f[cols].style.format({'Resultado Alcançado - Faturamento': 'R$ {:,}',
                                                    'Meta - Fatuamento': 'R$ {:,}',
                                                    'Resultado Alcançado - Lucro líquido': 'R$     {:,}',
                                                    'Meta - Lucro líquido': 'R$ {:,}',
                                                    }), use_container_width=True, hide_index=True,
                        column_config={
                                        "Porcentagem Alcançado - Faturamento": st.column_config.ProgressColumn(
                                                                                                "Porcentagem Alcançado - Faturamento",
                                                                                                help="Percentual alcançado das metas",
                                                                                                format="%.0f%%",
                                                                                                min_value=0,
                                                                                                max_value=100,
                                                                                            ),
                                        "Porcentagem Alcançado - Lucro líquido": st.column_config.ProgressColumn(
                                                                                                "Porcentagem Alcançado - Lucro líquido",
                                                                                                help="Percentual alcançado das metas",
                                                                                                format="%.0f%%",
                                                                                                min_value=0,
                                                                                                max_value=100,
                                                                                            ),
                                },
                        )

            st.title('')
            #Adicionar gráfico e filtro do contrato
            select_contratos = criar_selectBox(lista = df320_f['Contrato'].unique(), titulo='Filtro por Contratos',
                                            select_text = 'Escolha uma ou mais opções', tipo = 'multiselect', all_values=True)
            
            if dic_df['320'][dic_df['320']['contrato'].isin(select_contratos)]['id'].empty:
                pass
            else:
                df_contrato_fat, df_contrato_luc, meta_lucro_mensal, meta_fat_freq_mensal = okr_metrics.get_metas_mes(df_app=dic_df['320'], contrato=select_contratos)

                c31, c32 = st.columns([1,1], gap='large')
                # df_contrato
                with c31:
                    fig = fd.px_bar_chart(df=df_contrato_fat,x_axis='periodoDeAvaliacaomoeda',
                                        y_axis='resultadoAlcancadomoeda',texto=True, cor=roxo)
                    fig.update_layout(yaxis_title="FATURAMENTO (R$)", xaxis_title="MESES", title='Histórico do Faturamento')
                    # Adicionar a linha da meta
                    fig.add_trace(
                                go.Scatter(
                                    x=df_contrato_fat['periodoDeAvaliacaomoeda'],
                                    y=meta_fat_freq_mensal,
                                    line=dict(color=azul_b),
                                    name='Meta'
                                ))
                    st.plotly_chart(fig, use_container_width=True)
                with c32:
                    fig = fd.px_bar_chart(df=df_contrato_luc,x_axis='periodoDeAvaliacaomoeda', y_axis='resultadoAlcancadomoeda',texto=True, cor=laranja)
                    fig.update_layout(yaxis_title="LUCRO LÍQUIDO (R$)", xaxis_title="MESES", title='Histórico do Lucro')
                    # Adicionar a linha da meta
                    fig.add_trace(
                                go.Scatter(
                                    x=df_contrato_luc['periodoDeAvaliacaomoeda'],
                                    y=meta_lucro_mensal,
                                    line=dict(color=azul_b),
                                    name='Meta'
                                ))
                    st.plotly_chart(fig, use_container_width=True)
    
    
   