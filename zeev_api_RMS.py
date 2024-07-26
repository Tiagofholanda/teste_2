import requests
import pandas as pd
import streamlit as st
import numpy as np
import setup
import datetime
#def método GET
def zeev_request_get(base_url, params=None, **kwargs):
    response = requests.get(base_url, params=params, **kwargs)
    if response.status_code == 200:
        df = response.json()

        df = pd.json_normalize(df)

        return df
    else:
        print(response.json())

@st.cache_resource(show_spinner="Request API 1", ttl=datetime.timedelta(minutes=10))
def estrutura_api():
    from datetime import datetime
    df = []

    #variáveis globais
    token = st.secrets['authKey']
    url = st.secrets['url']
    endpoint = st.secrets['Endpoint']
    base_url = url+endpoint


    id_app_list = setup.id_app_list

    # Dados paginas
    page = 1

    # Lista de Atividades
    listTask = 'true'


    dataI = '2023-01-01'
    dataF = f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day}'

    for i in id_app_list:    
        headers = {'Authorization': token,
                   'Content-Type': 'application/json'}
        content = {
                'StartDateIntervalBegin': f'{dataI}',
                'StartDateIntervalEnd': f'{dataF}',
                'flowid' : f'{i}',
                'recordsPerPage': '30',
                'pageNumber': f'{page}',
                'showPendingInstanceTasks':f'{listTask}',
                'showFinishedInstanceTasks':f'{listTask}',
                'showPendingPendingAssignees':f'{listTask}'
                }
        try:
            json = zeev_request_get(base_url, params=content, headers=headers)
        except AttributeError:
            print('Verificar a função "zeev_request_get()", pois a mesma apresentou erro.')

        df.append(json)

    return df

@st.cache_resource(show_spinner="Tratamento API 1", ttl=datetime.timedelta(minutes=10))
def ajustes_api():
    # Carregando os dados
    try:
        df = estrutura_api()
    except AttributeError:
        print('Verificar a função "estrutura_api()", pois a mesma apresentou erro.')

    #unindo os dados em um data frame
    df_ = pd.concat(df, join='outer')

    # Abrindo coluna instace Task
    df_ = df_.explode('instanceTasks')
    
    # Retirando a coluna instace task do dataframe completo
    df_comp = df_.drop('instanceTasks', axis=1)

    # Transfomando o dicionário da coluna Instance Task em colunas do dataframe
    intanceTasks = df_['instanceTasks'].apply(pd.Series)

    # Adicionando prefixo a coluna Instance Task para não gerar inconsitência
    intanceTasks = intanceTasks.add_prefix('instanceTasks.')

    # Unindo o DataFrame
    df_ = pd.concat([df_comp, intanceTasks], axis=1)

    # Criando dataframe sem a coluna 'InstanceTasks.task'
    df_out_task = df_.drop('instanceTasks.task', axis=1)

    # Abrindo os dados da 'task'
    task = df_['instanceTasks.task'].apply(pd.Series)

    # Adicionando prefixo a coluna Task para não gerar inconsitência
    task = task.add_prefix('Tasks.')

    # Unindo o DataFrame
    df_ = pd.concat([df_out_task, task], axis=1)

    # Criando dataframe sem a coluna 'InstanceTasks.task'
    df_out_execut = df_.drop('instanceTasks.executor', axis=1)

    # Abrindo os dados da 'task'
    executor = df_['instanceTasks.executor'].apply(pd.Series)

    # Adicionando prefixo a coluna Task para não gerar inconsitência
    executor = executor.add_prefix('Executor.')

    # Unindo o DataFrame
    df_ = pd.concat([df_out_execut, executor], axis=1)

    # # Criando as colunas de Data e Tempo separadas
    # st.write(df_)
    # df_[['startDate', 'startTime']] = df_['startDateTime'].str.split('T', expand=True)
    # df_[['endDate', 'endTime']] = df_['endDateTime'].str.split('T', expand=True)
    # df_ = df_.drop(['startDateTime', 'endDateTime'], axis=1)

    # # Adicionando Coluna de Status do Ticket
    # df_['Status_Ticket'] = np.where(
    #     df_['endDate'].isnull(),
    #     'Em Andamento', 
    #     'Concluído'
    # )

    # df_['Status_Tarefa'] = np.where(
    #     df_['instanceTasks.active'] == True,
    #     'Em andamento',
    #     'Concluído'
    # )
    df_ = df_.apply(lambda x: x.astype(str).str.upper())
    return df_
