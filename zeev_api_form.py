import pandas as pd
import requests
import streamlit as st
import setup
import datetime

def explode_json_df(df) -> pd.DataFrame:
    # Procurar colunas que possuem json dentro de lista e dicionários
    df = df.reset_index()
    s = (df.applymap(type) == list).all()
    list_columns = s[s].index.tolist()
    
    s = (df.applymap(type) == dict).all()
    dict_columns = s[s].index.tolist()

    # Loop while enquanto exsistir colunas com diocionários dentro
    while len(list_columns) > 0 or len(dict_columns) > 0:
        for col in dict_columns:
            horiz_exploded = pd.json_normalize(df[col]).add_prefix(f'{col}.')
            horiz_exploded.index = df.index
            df = pd.concat([df, horiz_exploded], axis=1).drop(columns=[col])

        for col in list_columns:
            df = df.drop(columns=[col]).join(df[col].explode().apply(pd.Series).add_prefix('formFields.'))

        s = (df.applymap(type) == list).all()
        list_columns = s[s].index.tolist()

        s = (df.applymap(type) == dict).all()
        dict_columns = s[s].index.tolist()
    return df

def zeev_request_get(base_url, params=None, **kwargs) -> pd.DataFrame:
    response = requests.get(base_url, params=params, **kwargs)

    if response.status_code == 200:
        df = response.json()
        df = pd.json_normalize(df)

        if df.empty:
            return df
        else:
            # Formatar o dataframe
            df = explode_json_df(df)
            
        return df
    
    else:
        print(response.json())

@st.cache_resource(show_spinner="Request API", ttl=datetime.timedelta(minutes=10))
def estrutura_api() -> pd.DataFrame:
    from datetime import datetime
    import math
    dic_df = {}

    #variáveis globais
    token = st.secrets['authKey']
    url = st.secrets['url']
    endpoint = st.secrets['Endpoint']
    base_url = url+endpoint


    id_app_list = setup.id_app_list

    # Dados paginas
    page = 1

    dataI = '2023-01-01'
    dataF = f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day}'


    for i in id_app_list:
        df_concat = []
        for pg in range(1,11):
            try:
                # Lista de Atividades
                formField = setup.dic_formfield[i]    
                tam_max = 45
                
                # Caso o formField tenha mais indentadores do que o tamanho máx de 45. Iremos quebrar a requisição em "n" partes
                if len(formField)>tam_max:
                    div = math.ceil(len(formField)/tam_max)
                    dfs = []
                    
                    # Loop para fazer a requisição por partes
                    for n in range(1, div+1):
                        lista_id = formField[tam_max*(n-1):tam_max*n]
                        
                        headers = {'Authorization': token,
                                'Content-Type': 'application/json'}
                        content = {
                            'StartDateIntervalBegin': f'{dataI}',
                                'StartDateIntervalEnd': f'{dataF}',
                                'flowid' : f'{i}',
                                'recordsPerPage': '100',
                                'pageNumber': f'{pg}',
                                'formFieldNames':lista_id,
                                'simulation':False
                                }
                        try:
                            json = zeev_request_get(base_url, params=content, headers=headers)
                            
                            if json.empty:
                                pass
                            else:
                                df_ = formata_forms_df(df_ = json)
                                dfs.append(df_)
                        except AttributeError:
                            print('Verificar a função "zeev_request_get()", pois a mesma apresentou erro.')
                    if len(dfs)==0:
                        pass
                    else:
                        df = pd.concat(dfs)
                        df = df.groupby('id').first().reset_index()

                else:
                    headers = {'Authorization': token,
                            'Content-Type': 'application/json'}
                    content = {
                            'StartDateIntervalBegin': f'{dataI}',
                            'StartDateIntervalEnd': f'{dataF}',
                            'flowid' : f'{i}',
                            'recordsPerPage': '100',
                            'pageNumber': f'{pg}',
                            'formFieldNames':formField,
                            'simulation':False
                            }
                    try:
                        json = zeev_request_get(base_url, params=content, headers=headers)
                        
                        if json.empty:
                            df = pd.DataFrame()                         
                        else: 
                            df = formata_forms_df(df_ = json)
                            
                        
                    except AttributeError:
                        print('Verificar a função "zeev_request_get()", pois a mesma apresentou erro.')
                #atribuir o dataframe ao dicionário dos apps
                df_concat.append(df.apply(lambda x: x.astype(str).str.upper()))
            except:
                df_concat.append(pd.DataFrame(['vazio']))
        
        df_result = pd.concat(df_concat)
        dic_df[i] = df_result
    
    return dic_df

def formata_forms_df(df_) -> pd.DataFrame:
    
    df_ = df_.pivot(
        index=df_.columns[~(df_.columns.isin({'formFields.name','formFields.value','formFields.id'}))],
        columns='formFields.name',
        values='formFields.value'
    )

    df_ = df_.reset_index(level=0, drop=True).reset_index()
    
    return df_

@st.cache_resource(show_spinner="Tratamento dados Zeev forms", ttl=datetime.timedelta(minutes=10))
def ajustes_api() -> pd.DataFrame:
    # Carregando os dados
    dic_df = estrutura_api()
    dic_df['320']['resultadoAlcancadomoeda'] = dic_df['320']['resultadoAlcancadomoeda'].str.replace('.', '')
    dic_df['320']['resultadoAlcancadomoeda'] = dic_df['320']['resultadoAlcancadomoeda'].str.replace(',', '.').astype(float)
    dic_df['320']['diretoria'] = dic_df['320']['diretoria'].str.replace('DDIAT -DIRETORIA DE DESL. INVOL. E ANÁLISE TERRIT.', 'DDIAT - DIRETORIA DE DESL. INVOL. E ANÁLISE TERRIT.')
    
    dic_df['315']['resultadoAlcancadomoeda'] = dic_df['315']['resultadoAlcancadomoeda'].str.replace('.', '')
    dic_df['315']['resultadoAlcancadomoeda'] = dic_df['315']['resultadoAlcancadomoeda'].str.replace(',', '.').astype(float)
    dic_df['315']['totalAcumulado'] = dic_df['315']['totalAcumulado'].str.replace('.', '')
    dic_df['315']['totalAcumulado'] = dic_df['315']['totalAcumulado'].str.replace(',', '.').astype(float)     

    
    return dic_df
