from logging.handlers import DEFAULT_SOAP_LOGGING_PORT
from re import S
import pandas as pd
import numpy as np
import streamlit as st
import setup
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

@st.cache_resource(show_spinner="Calculando...", ttl=datetime.timedelta(minutes=10))
def formata_df_geral(df_, diretoria):
    df_ = df_.loc[df_['DiretoriaCompartilha'].str.contains(diretoria, na=False)]
    cols292 = ['index','Diretoria', 'oKR', 'kR', 'nivelDeDesdobramento', 'DiretoriaCompartilha','ColaboradorResponsavel','metaIndividual',
               'TipoMedida','periodo','frequenciaDeMensuracao', 'Meta', 'Resultado', 'PorcentagemAlcancada']
    df_.rename(columns={
        'kR':'KR',
        'oKR': 'OKR',
        'nivelDeDesdobramento':'Nivel de Desdobramento',
        'metaIndividual':'Meta Individual',
        'DiretoriaCompartilha':'Diretorias que participam',
        'TipoMedida':'Tipo de medida',
        'periodo': 'Periodo',
        'frequenciaDeMensuracao': 'Frequência de Mensuração',
        'Meta':'Meta',
        'ColaboradorResponsavel':'Colaborador',
        'Resultado':'Resultado',
        'PorcentagemAlcancada':'Porcentagem Alcançada'
    }, inplace=True)
    df_['Meta Individual'] = df_['index'].astype(str)+' - '+df_['Meta Individual'].astype(str)
    df_ = df_.sort_values(by='Porcentagem Alcançada')
    df_['Resultado'] = df_['Resultado'].fillna(0)
    df_['Porcentagem Alcançada'] = df_['Porcentagem Alcançada'].fillna(0)
    return df_[['Diretoria','OKR','KR','Nivel de Desdobramento','Colaborador','Diretorias que participam','Meta Individual',
                'Tipo de medida','Periodo','Frequência de Mensuração', 'Meta', 'Resultado', 'Porcentagem Alcançada']]

@st.cache_resource(show_spinner="Calculando...", ttl=datetime.timedelta(minutes=10))
def format_outras_metas(df292, df315):

    cols292 = ['index','Diretoria', 'oKR', 'kR', 'nivelDeDesdobramento', 'DiretoriaCompartilha',
               'ColaboradorResponsavel','metaIndividual','TipoMedida','periodo','frequenciaDeMensuracao', 'Meta', 'Resultado', 'PorcentagemAlcancada']
  
    df_ = pd.concat([df292[cols292],df315[cols292]])
    df_.rename(columns={
        'kR':'KR',
        'oKR': 'OKR',
        'nivelDeDesdobramento':'Nivel de Desdobramento',
        'metaIndividual':'Meta Individual',
        'DiretoriaCompartilha':'Diretorias que participam',
        'TipoMedida':'Tipo de medida',
        'periodo': 'Periodo',
        'frequenciaDeMensuracao': 'Frequência de Mensuração',
        'Meta':'Meta',
        'ColaboradorResponsavel':'Colaborador',
        'Resultado':'Resultado',
        'PorcentagemAlcancada':'Porcentagem Alcançada'
    }, inplace=True)
    df_['Meta Individual'] = df_['index'].astype(str)+' - '+df_['Meta Individual'].astype(str)
    df_ = df_.sort_values(by='Porcentagem Alcançada')
    df_['Resultado'] = df_['Resultado'].fillna(0)
    df_['Porcentagem Alcançada'] = df_['Porcentagem Alcançada'].fillna(0)
    return df_[['Diretoria','OKR','KR','Nivel de Desdobramento','Colaborador','Diretorias que participam','Meta Individual',
                'Tipo de medida','Periodo','Frequência de Mensuração', 'Meta', 'Resultado', 'Porcentagem Alcançada']]

@st.cache_resource(show_spinner="Calculando Faturamento e Lucro por Diretoria mensal...", ttl=datetime.timedelta(minutes=10))
def get_metas_mes(df_app, contrato):
    import re
    id_ = list(df_app[df_app['contrato'].isin(contrato)]['id'].unique())
  
    cols = ['cumpriuAMetamoeda', 'discriminacaoDoResultadoobservacoesmoeda', 'necessidadeDePlanoDeAcaomoeda', 'periodoDeAvaliacaomoeda']

    try:
        df_contrato = df_app[df_app['id'].isin(id_)][['diretoria','cumpriuAMetamoeda',
                                        'detalhamentoDaMetaGeralFaturamento',
                                        'detalhamentoDaMetaGeralLucroLiquido',
                                        'discriminacaoDoResultadoobservacoesmoeda', 'frequenciaDeMensuracao','periodo',
                                        'kR', 'metaGeralFaturamento', 'metaGeralLucroLiquido',
                                        'necessidadeDePlanoDeAcaomoeda', 'oKR',
                                        'peso', 'responsavelPelaAtividadeval', 'periodoDeAvaliacaomoeda','resultadoAlcancadomoeda']]
        
    except:
        df_contrato = df_app[df_app['id'].isin(id_)][['diretoria','detalhamentoDaMetaGeralFaturamento',
                                            'detalhamentoDaMetaGeralLucroLiquido', 'frequenciaDeMensuracao','periodo',
                                            'kR', 'metaGeralFaturamento', 'metaGeralLucroLiquido','oKR',
                                            'peso', 'responsavelPelaAtividadeval','resultadoAlcancadomoeda']]
        for c in cols:
            df_contrato[c]=np.nan
    try:
        df_contrato_fat = df_app[(df_app['id'].isin(id_))&
                        (df_app['tipo'].str.contains('FATURAMENTO BRUTO'))][['diretoria','kR','cumpriuAMetamoeda',
                                    'detalhamentoDaMetaGeralFaturamento',
                                    'detalhamentoDaMetaGeralLucroLiquido',
                                    'discriminacaoDoResultadoobservacoesmoeda', 'frequenciaDeMensuracao','periodo', 'metaGeralFaturamento', 'metaGeralLucroLiquido',
                                    'necessidadeDePlanoDeAcaomoeda', 'oKR',
                                    'peso', 'responsavelPelaAtividadeval', 'periodoDeAvaliacaomoeda','resultadoAlcancadomoeda','tipo']]
    except:
        df_contrato_fat = df_app[(df_app['id'].isin(id_))&
                        (df_app['tipo'].str.contains('FATURAMENTO BRUTO'))][['diretoria','kR','detalhamentoDaMetaGeralFaturamento',
                                    'detalhamentoDaMetaGeralLucroLiquido', 'frequenciaDeMensuracao','periodo', 'metaGeralFaturamento', 'metaGeralLucroLiquido', 'oKR',
                                    'peso', 'responsavelPelaAtividadeval','resultadoAlcancadomoeda','tipo']]
        for c in cols:
            df_contrato_fat[c]=np.nan
    try:
        df_contrato_luc = df_app[(df_app['id'].isin(id_))&
                        (df_app['tipo'].str.contains('LUCRO LÍQUIDO'))][['diretoria','kR','cumpriuAMetamoeda',
                                    'detalhamentoDaMetaGeralFaturamento',
                                    'detalhamentoDaMetaGeralLucroLiquido',
                                    'discriminacaoDoResultadoobservacoesmoeda', 'frequenciaDeMensuracao','periodo', 'metaGeralFaturamento', 'metaGeralLucroLiquido',
                                    'necessidadeDePlanoDeAcaomoeda', 'oKR',
                                    'peso', 'responsavelPelaAtividadeval', 'periodoDeAvaliacaomoeda','resultadoAlcancadomoeda','tipo']]
    except:
        df_contrato_luc = df_app[(df_app['id'].isin(id_))&
                        (df_app['tipo'].str.contains('LUCRO LÍQUIDO'))][['diretoria','kR','detalhamentoDaMetaGeralFaturamento',
                                    'detalhamentoDaMetaGeralLucroLiquido', 'frequenciaDeMensuracao','periodo', 'metaGeralFaturamento', 'metaGeralLucroLiquido', 'oKR',
                                    'peso', 'responsavelPelaAtividadeval','resultadoAlcancadomoeda','tipo']]
        for c in cols:
            df_contrato_luc[c]=np.nan
    
    meta_fat_freq = df_contrato['detalhamentoDaMetaGeralFaturamento'].str.replace(',','.')
    r_fat = []
    for v in meta_fat_freq:
        try:
            
            r_fat.append(float(re.findall("\d+\.\d+", v.replace(',','.'))[0])*1000000)
            
        except IndexError:
            
            r_fat.append(0)

    meta_fat_freq = sum(r_fat)

    meta_lucro_freq = df_contrato['detalhamentoDaMetaGeralLucroLiquido'].str.replace(',','.')

    r_luc = []
    for v in meta_lucro_freq:
        try:
            r_luc.append(float(re.findall("\d+\.\d+", v.replace(',','.'))[0])*1000000)
            
        except IndexError:
            r_luc.append(0)
    
    meta_lucro_freq = sum(r_luc)

    meta_lucro_mensal = [meta_lucro_freq]*(12)
    meta_fat_freq_mensal = [meta_fat_freq]*(12)

    df_contrato_luc_g = df_contrato_luc.groupby('periodoDeAvaliacaomoeda')['resultadoAlcancadomoeda'].sum().reset_index()
    df_contrato_fat_g = df_contrato_fat.groupby('periodoDeAvaliacaomoeda')['resultadoAlcancadomoeda'].sum().reset_index()
    return df_contrato_fat_g, df_contrato_luc_g, meta_lucro_mensal, meta_fat_freq_mensal

@st.cache_resource(show_spinner="Calculando Vendas por Diretoria mensal...", ttl=datetime.timedelta(minutes=10))
def get_metas_mes_vendas(df_app):
    import re
    cols = ['cumpriuAMetamoeda', 'discriminacaoDoResultadoobservacoesmoeda', 'necessidadeDePlanoDeAcaomoeda', 'periodoDeAvaliacaomoeda']

    try:
        df_contrato = [['cumpriuAMetamoeda',
                                        'detalhamentoDaMetaGeralFaturamento',
                                        'detalhamentoDaMetaGeralLucroLiquido',
                                        'discriminacaoDoResultadoobservacoesmoeda', 'frequenciaDeMensuracao',
                                        'kR', 'metaGeralFaturamento', 'metaGeralLucroLiquido',
                                        'necessidadeDePlanoDeAcaomoeda', 'oKR',
                                        'peso', 'responsavelPelaAtividadeval', 'periodoDeAvaliacaomoeda','resultadoAlcancadomoeda']]
        
    except:
        df_contrato = DEFAULT_SOAP_LOGGING_PORT[['detalhamentoDaMetaGeralFaturamento',
                                        'detalhamentoDaMetaGeralLucroLiquido', 'frequenciaDeMensuracao',
                                        'kR', 'metaGeralFaturamento', 'metaGeralLucroLiquido','oKR',
                                        'peso', 'responsavelPelaAtividadeval','resultadoAlcancadomoeda']]
        for c in cols:
            df_contrato[c]=np.nan
    try:
        df_contrato_fat = df_app[(df_app['id'].str.contains(id_))&
                        (df_app['tipo'].str.contains('FATURAMENTO BRUTO'))][['kR','cumpriuAMetamoeda',
                                    'detalhamentoDaMetaGeralFaturamento',
                                    'detalhamentoDaMetaGeralLucroLiquido',
                                    'discriminacaoDoResultadoobservacoesmoeda', 'frequenciaDeMensuracao', 'metaGeralFaturamento', 'metaGeralLucroLiquido',
                                    'necessidadeDePlanoDeAcaomoeda', 'oKR',
                                    'peso', 'responsavelPelaAtividadeval', 'periodoDeAvaliacaomoeda','resultadoAlcancadomoeda','tipo']]
    except:
        df_contrato_fat = df_app[(df_app['id'].str.contains(id_))&
                        (df_app['tipo'].str.contains('FATURAMENTO BRUTO'))][['kR','detalhamentoDaMetaGeralFaturamento',
                                    'detalhamentoDaMetaGeralLucroLiquido', 'frequenciaDeMensuracao', 'metaGeralFaturamento', 'metaGeralLucroLiquido', 'oKR',
                                    'peso', 'responsavelPelaAtividadeval','resultadoAlcancadomoeda','tipo']]
        for c in cols:
            df_contrato_fat[c]=np.nan
    try:
        df_contrato_luc = df_app[(df_app['id'].str.contains(id_))&
                        (df_app['tipo'].str.contains('LUCRO LÍQUIDO'))][['kR','cumpriuAMetamoeda',
                                    'detalhamentoDaMetaGeralFaturamento',
                                    'detalhamentoDaMetaGeralLucroLiquido',
                                    'discriminacaoDoResultadoobservacoesmoeda', 'frequenciaDeMensuracao', 'metaGeralFaturamento', 'metaGeralLucroLiquido',
                                    'necessidadeDePlanoDeAcaomoeda', 'oKR',
                                    'peso', 'responsavelPelaAtividadeval', 'periodoDeAvaliacaomoeda','resultadoAlcancadomoeda','tipo']]
    except:
        df_contrato_luc = df_app[(df_app['id'].str.contains(id_))&
                        (df_app['tipo'].str.contains('LUCRO LÍQUIDO'))][['kR','detalhamentoDaMetaGeralFaturamento',
                                    'detalhamentoDaMetaGeralLucroLiquido', 'frequenciaDeMensuracao', 'metaGeralFaturamento', 'metaGeralLucroLiquido', 'oKR',
                                    'peso', 'responsavelPelaAtividadeval','resultadoAlcancadomoeda','tipo']]
        for c in cols:
            df_contrato_luc[c]=np.nan

    meta_fat_freq = df_contrato['detalhamentoDaMetaGeralFaturamento'].values[0]
    meta_fat_freq = float(re.findall("\d+\.\d+", meta_fat_freq.replace(',','.'))[0])*1000000
    meta_lucro_freq = df_contrato['detalhamentoDaMetaGeralLucroLiquido'].values[0]
    meta_lucro_freq = float(re.findall("\d+\.\d+", meta_lucro_freq.replace(',','.'))[0])*1000000
    meta_lucro_mensal = [meta_lucro_freq]*(12)
    meta_fat_freq_mensal = [meta_fat_freq]*(12)
   
    return df_contrato_fat, df_contrato_luc, meta_lucro_mensal, meta_fat_freq_mensal


@st.cache_resource(show_spinner="Calculando Faturamento e Lucro por Diretoria...", ttl=datetime.timedelta(minutes=10))
def calcula_faturamento_lucro_por_diretoria(df320, exportar_dic=True):
    df_g = df320.groupby('Diretoria')[['metaGeralFaturamento', 'metaGeralLucroLiquido',
                                            'resultadoAlcancadoFaturamento', 'resultadoAlcancadoLucro']].sum().reset_index()
    df_g
    # Calcular a PorcentagemAlcancada
    df_g['PorcentagemAlcancadaFaturamento'] = round((df_g['resultadoAlcancadoFaturamento']/df_g['metaGeralFaturamento'])*100,1)
    df_g['PorcentagemAlcancadaLucro'] = round((df_g['resultadoAlcancadoLucro']/df_g['metaGeralLucroLiquido'])*100,1)

    df_g['resultadoAlcancadoLucroMM'] = (round(df_g['resultadoAlcancadoLucro']/1000000,2)).astype(str)+' MM'
    df_g['resultadoAlcancadoFaturamentoMM'] = (round(df_g['resultadoAlcancadoFaturamento']/1000000,2)).astype(str)+' MM'

    if exportar_dic:
        # Calcular valor por diretoria
        dic = {}
        for diretoria in ['DASA', 'DDIAT', 'DES', 'DAF', 'DPUB', 'DCOM', 'DRF']:
            if diretoria=='DAF' or diretoria=='DCOM':
                dic[diretoria] = ['0.0 MM', '0.0 MM', 0.0, 0.0]
            else:
                fat = df_g[df_g['Diretoria'].str.contains(diretoria+' - ')]['resultadoAlcancadoFaturamentoMM'].values[0]
                lucro = df_g[df_g['Diretoria'].str.contains(diretoria+' - ')]['resultadoAlcancadoLucroMM'].values[0]
                try:
                    pctfat = int(df_g[df_g['Diretoria'].str.contains(diretoria+' - ')]['PorcentagemAlcancadaFaturamento'].values[0])
                except:
                    pctfat = 0.0
                try:
                    pctlucro = int(df_g[df_g['Diretoria'].str.contains(diretoria+' - ')]['PorcentagemAlcancadaLucro'].values[0])
                except:
                    pctlucro=0.0
                dic[diretoria] = [fat, lucro, pctfat, pctlucro]
            
            # try:
                
            #     fat = df_g[df_g['Diretoria'].str.contains(diretoria+' - ')]['resultadoAlcancadoFaturamentoMM'].values[0]
            #     lucro = df_g[df_g['Diretoria'].str.contains(diretoria+' - ')]['resultadoAlcancadoLucroMM'].values[0]
            #     pctfat = int(df_g[df_g['Diretoria'].str.contains(diretoria+' - ')]['PorcentagemAlcancadaFaturamento'].values[0])
            #     pctlucro = int(df_g[df_g['Diretoria'].str.contains(diretoria+' - ')]['PorcentagemAlcancadaLucro'].values[0])
            #     dic[diretoria] = [fat, lucro, pctfat, pctlucro]
            #     st.write(dic)
            # except:
            #     dic[diretoria] = ['0.0 MM', '0.0 MM', 0.0, 0.0]

        return df_g, dic
    else:
        return df_g

@st.cache_resource(show_spinner="Calculando Faturamento e Lucro por Diretoria...", ttl=datetime.timedelta(minutes=10))
def calcula_vendas_por_diretoria(df315, exportar_dic=True):
    df_g = df315.groupby('Diretoria')[['Meta', 'Resultado']].sum().reset_index()
    # Calcular a PorcentagemAlcancada
    df_g['PorcentagemAlcancada'] = round((df_g['Resultado']/df_g['Meta'])*100,1)

    if exportar_dic:
        # Calcular valor por diretoria
        dic = {}
        for diretoria in ['DASA', 'DDIAT', 'DES', 'DAF', 'DPUB', 'DCOM']:
            try:
                vendas = df_g[df_g['Diretoria'].str.contains(diretoria)]['PorcentagemAlcancada'].values[0]
                dic[diretoria] = vendas
            except:
                dic[diretoria] = 0
        return df_g, dic
    else:
        return df_g

@st.cache_resource(show_spinner="Calculando Faturamento e Lucro...", ttl=datetime.timedelta(minutes=10))
def get_df_faturamento_lucro(dic_df, app='320'):
    import re
    df_app = dic_df[app].copy()
    df_left = df_app[['id', 'masterInstanceId', 'diretoria','contrato','kR', 'oKR', 'metaGeralFaturamento',
            'metaGeralLucroLiquido', 'responsavelPelaAtividadeval', 'prazoParaExecucaoRDN', 'periodo','peso']].replace('NAN', np.nan).dropna()


    #remover esta correção
    try:
        df_app['tipo'].replace('', 'LUCRO LÍQUIDO', inplace=True)
    except:
        df_app['tipo'] = 'NA'
 
    df_g = df_app[['id','kR','resultadoAlcancadomoeda','tipo']].groupby(['id','tipo']).sum()\
                                                        .reset_index()
    

    dfs = []
    for i, c in zip(['FATURAMENTO BRUTO', 'LUCRO LÍQUIDO'], ['resultadoAlcancadoFaturamento', 'resultadoAlcancadoLucro']):
        aux = df_g.loc[df_g['tipo']==i][['id', 'resultadoAlcancadomoeda']].set_index('id')
        aux.columns = [c]
        dfs.append(aux)
    df_right = pd.concat(dfs, axis=1)
    df_right = df_right.reset_index()
     

    df_resultado = df_left.merge(df_right, on='id', how='left')
    
    #formatar campo metaFaturamento e metaLucro
    df_resultado['metaGeralFaturamento'] = df_resultado['metaGeralFaturamento'].str.replace(',', '.')
    df_resultado['metaGeralLucroLiquido'] = df_resultado['metaGeralLucroLiquido'].str.replace(',', '.')
    try:
        df_resultado['metaGeralFaturamento'] = [float(re.findall("\d+\.\d+", x)[0])*1000000 for x in df_resultado['metaGeralFaturamento']]
    except:
        df_resultado['metaGeralFaturamento'] = [float(re.findall("\d+", x)[0])*1000000 for x in df_resultado['metaGeralFaturamento']]
    try:
        df_resultado['metaGeralLucroLiquido'] = [float(re.findall("\d+\.\d+", x)[0])*1000000 for x in df_resultado['metaGeralLucroLiquido']]
    except:
        df_resultado['metaGeralLucroLiquido'] = [float(re.findall("\d+", x)[0])*1000000 for x in df_resultado['metaGeralLucroLiquido']]

    # Calcular a PorcentagemAlcancada
    df_resultado['PorcentagemAlcancadaFaturamento'] = (df_resultado['resultadoAlcancadoFaturamento']/df_resultado['metaGeralFaturamento'])*100
    df_resultado['PorcentagemAlcancadaLucro'] = (df_resultado['resultadoAlcancadoLucro']/df_resultado['metaGeralLucroLiquido'])*100
    df_resultado.rename(columns={
            'id':'index',
            'diretoria': 'Diretoria'
        }, inplace=True)
    
    df_resultado['resultadoAlcancadoFaturamento'] = round(df_resultado['resultadoAlcancadoFaturamento'],2)
    df_resultado['resultadoAlcancadoLucro'] = round(df_resultado['resultadoAlcancadoLucro'],2)
    return df_resultado

# @st.cache_resource(show_spinner="Calculando Faturamento e Lucro..", ttl=datetime.timedelta(minutes=10))
# def get_contrato(dic_df, app='289'):
#     '''
#         Extair o nome dos contratos no app 289 - Desdobramento
#     '''
#     import numpy as np
#     df_app = dic_df[app]
#     contratos = []
#     for row in df_app['metaIndividualtab'].str.split(' = '):
#         if len(row)>1:
#             contratos.append(row[0])
#         else:
#             contratos.append(np.nan)
#     return contratos

@st.cache_resource(show_spinner="Processando dados das metas...", ttl=datetime.timedelta(minutes=10))
def df_to_dash(df_metas)->pd.DataFrame:
    df_g=df_metas.groupby(by=['Diretoria', 'kR']).agg({'oKR': 'sum', 'Meta': 'sum', 'Resultado': 'sum', 'peso': 'mean'})
    df_g['PorcentagemAlcancada'] = (df_g['Resultado']/df_g['Meta'])*100
    return df_g

@st.cache_resource(show_spinner="Cálculo das metas...", ttl=datetime.timedelta(minutes=10))
# Calcular progresso metas
def get_df_metas(dic_df, app='292'):
    '''
        Gerar BD das metas e resultados finais
        
    '''
    import numpy as np
    import re
    df_app = dic_df[app]
    dic = {}
    dic_val_metas = {}
    
    for id_ in df_app['id'].unique():
        df_app_id = df_app.loc[df_app['id']==id_]
        medida = df_app_id['tipoDeMedida'].values[0]
        col_result = setup.tipo_medida[medida]
        col_vazio = setup.campo_vazio_medida[medida]
        try:
            dic[id_] = df_app_id[col_result]
        except:
            for col in col_vazio:
                if col=='resultadoAlcancadoSimnaoentreg':
                    df_app_id[col] = 'NÃO'
                else:
                    df_app_id[col] = np.nan
            dic[id_] = df_app_id[col_result]

        # valor da meta
        t = dic[id_]['metaIndividual'].values[0].replace(',','.')
        if len(t.split(' = '))>1:
            contratos = t.split(' = ')[0]
        else:
            contratos = np.nan

        if medida == 'UNIDADE MONETÁRIA (R$)':
            if len(re.findall("\d+\.\d+", t))!=0:
                try:
                    valor_meta = [float(re.findall("\d+\.\d+", t)[0])*1000000, float(dic[id_][col_result[-1]].values[0].replace('.', '',).replace(',', '.',))]
                except:
                    valor_meta = [float(re.findall("\d+\.\d+", t)[0])*1000000, float(dic[id_][col_result[-1]].replace('', np.nan).values[0])]
            elif len(re.findall("\d+", t))!=0:
                try:
                    valor_meta = [float(re.findall("\d+", t)[0])*1000000, float(dic[id_][col_result[-1]].values[0].replace('.', '',).replace(',', '.',))]
                except:
                    valor_meta = [float(re.findall("\d+", t)[0])*1000000, float(dic[id_][col_result[-1]].replace('', np.nan).values[0])]

        elif medida == 'QUANTIDADE (UND.)':
            try:
                valor_meta = [int(re.findall("\d+", t)[0]), float(dic[id_][col_result[-1]].values[0].replace('.', '',).replace(',', '.',))]
            except:
                
                try:
                    valor_meta = [int(re.findall("\d+", t)[0]), float(dic[id_][col_result[-1]].replace('', np.nan).values[0])]
                except:
                    valor_meta = [np.nan, float(dic[id_][col_result[-1]].replace('', np.nan).values[0])]
        
        elif medida == 'PORCENTAGEM (%)':
            try:
                valor_meta = [float(re.findall("\d+", t)[0]), float(dic[id_][col_result[-1]].values[0].replace('.', '',).replace(',', '.',))]
            except:
                
                try:
                    valor_meta = [float(re.findall("\d+", t)[0]), float(dic[id_][col_result[-1]].replace('', np.nan).values[0])]
                except:
                    valor_meta = [np.nan, float(dic[id_][col_result[-1]].replace('', np.nan).values[0])]
        else:
            boolSimNao = dic[id_]['resultadoAlcancadoSimnaoentreg'].str.contains('SIM').any()
            if boolSimNao==True:
                restultado = 1
            else:
                restultado = 0
            valor_meta = [1, restultado]
            
        # Calcular % meta
        # Filtro quanto menor a porcentagem melhor
        if t.__contains__('TURN OVER'):
            percent = (valor_meta[0]/valor_meta[1])*100
        else:
            percent = (valor_meta[1]/valor_meta[0])*100

        valor_meta.append(round(percent,1))
        # adicionar medida
        valor_meta.append(medida)
        # adicionar diretoria
        valor_meta.append(dic[id_]['diretoria'].values[0])
        # adicionar colaborador
        valor_meta.append(dic[id_]['colaboradorResponsavel'].values[0])
        # adicionar diretorias compartilha meta
        d = dic[id_]['diretoriasQueParticipamDessaMeta'].replace('', np.nan)\
                                                        .replace('NAN', np.nan)\
                                                        .dropna().unique()
        d_str = '; '.join(d)
        valor_meta.append(d_str)
        # adicionar quantidade de diretorias compartilha meta
        qtd_share = len(d)
        valor_meta.append(qtd_share)
        # Inserir Contrato no início
        valor_meta.insert(0,contratos)
        # Inserir peso no início 'peso'
        valor_meta.insert(0,int(dic[id_]['peso'].values[0])/100)
        # inserir nivelDeDesdobramento
        valor_meta.insert(0,dic[id_]['nivelDeDesdobramento'].values[0])
        # Inserir meta infividual metaIndividual
        valor_meta.insert(0,dic[id_]['metaIndividual'].values[0])
        # Inserir KR no início 'kR'
        valor_meta.insert(0,dic[id_]['kR'].values[0])
        # Inserir o OKR
        valor_meta.insert(0,dic[id_]['oKR'].values[0])
        # Inserir masterinstanceID
        valor_meta.insert(0,dic[id_]['masterInstanceId'].values[0])
         # adicionar periodo
        valor_meta.insert(0,dic[id_]['periodo'].values[0])
        # adicionar frequÊncia
        valor_meta.insert(0,dic[id_]['frequenciaDeMensuracao'].values[0])

        dic_val_metas[id_] = valor_meta
    df_metas = pd.DataFrame(dic_val_metas, index=['frequenciaDeMensuracao','periodo', 'masterInstanceId','oKR','kR','metaIndividual','nivelDeDesdobramento','peso','Contrato','Meta','Resultado', 'PorcentagemAlcancada', 'TipoMedida', 'Diretoria',
                                                    'ColaboradorResponsavel', 'DiretoriaCompartilha', 'Qtd DiretoriaCompartilha']).T
    df_metas.reset_index(inplace=True)
    df_metas['ColaboradorResponsavel'] = df_metas['ColaboradorResponsavel'].replace(setup.replace_emails)
    return df_metas, dic

def soma_ponderada(lista, pesos):
    resultado = np.sum(lista*pesos)
    return resultado

def calc_percentual_alcance(df):
    pass

#@st.cache_data(show_spinner="Gráfico de linha2", ttl=datetime.timedelta(minutes=10))
def plot_line_acompanhamento(val1, val2):
    import plotly.graph_objects as go
    import numpy as np

    title = 'Main Source for News'
    labels = ['Planejado', 'Alcançado']
    colors = ['rgb(115,115,115)', azul_b]

    mode_size = [10, 15]
    line_size = [2, 6]

    x_data = np.vstack((np.arange(1, 13),)*2)

    y_data = np.array([
        val1,
        val2
    ])

    fig = go.Figure()

    for i in range(0, 2):
        fig.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines',
            name=labels[i],
            line=dict(color=colors[i], width=line_size[i]),
            connectgaps=True,
        ))
        
        # endpoints
        fig.add_trace(go.Scatter(
            x=[x_data[i][0], x_data[i][-1]],
            y=[y_data[i][0], y_data[i][-1]],
            mode='markers',
            marker=dict(color=colors[i], size=mode_size[i])
        ))

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    annotations = []

    # Adding labels
    for y_trace, label, color in zip(y_data, labels, colors):
        # labeling the left_side of the plot
        if label=='Planejado':
            annotations.append(dict(xref='paper', x=0.05, y=8,
                                        xanchor='right', yanchor='middle',
                                        text=label + ' {}%'.format(y_trace[0]),
                                        font=dict(family='Arial',
                                                  size=16,
                                                  color=color),
                                        showarrow=False))
        else:
            annotations.append(dict(xref='paper', x=0.05, y=y_trace[0],
                                        xanchor='right', yanchor='middle',
                                        text=label + ' {}%'.format(y_trace[0]),
                                        font=dict(family='Arial',
                                                  size=16,
                                                  color=color),
                                        showarrow=False))
        # labeling the right_side of the plot
        annotations.append(dict(xref='paper', x=0.95, y=y_trace[-1],
                                    xanchor='left', yanchor='middle',
                                    text='{}%'.format(y_trace[-1]),
                                    font=dict(family='Arial',
                                                size=16),
                                    showarrow=False))
    

    fig.update_layout(annotations=annotations)
    fig.update_layout(title_text='Progresso das metas')
    st.plotly_chart(fig, use_container_width=True)

def hex_to_rgb(hex_color: str, opacity) -> tuple:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = hex_color * 2
    return int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16), opacity

#@st.cache_data(show_spinner="Gráfico de barra", ttl=datetime.timedelta(minutes=10))
def ploty_bar(x=['Metas concluídas', 'Metas em andamento'], y=[20,80]):
    import plotly.graph_objects as go

    colors = [azul_b, laranja]

    fig = go.Figure(data=[go.Bar(
        x=x,
        y=y,
        marker_color=colors # marker color can be a single color value or an iterable
    )])
    fig.update_layout(title_text='Metas alcalçadas x Andamento')

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)