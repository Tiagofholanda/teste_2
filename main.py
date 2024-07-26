import pandas as pd
import datetime
import streamlit as st
from streamlit_option_menu import option_menu # type: ignore
import yaml
from yaml import SafeLoader
from streamlit_authenticator  import Authenticate # type: ignore
import os
import base64
import setup
import pg_okr_geral
import pg_okr_diretoria
import zeev_api_RMS as za
import zeev_api_form as zf

# 'OKR':'@Okr2024'
# Cores NMC
roxo = "#45277f"
laranja = "#f0a800"
azul = "#11a4df"
azul_b = "#252859"
vermelho = "#e9501b"
verde = "#148135"
amarelo = "#ddd424"
paleta_IVS = [azul_b,azul, amarelo, laranja, vermelho]
paleta_NMC = [roxo, laranja, azul, vermelho, azul_b, verde,amarelo]

#@st.cache_resource(show_spinner="Conectando ao ambiente NMC..", ttl=datetime.timedelta(hours=2))

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

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def img_to_sidebar():
    img = get_img_as_base64("./img/img_sidebar.png")
    page_bg_img = f"""
                <style>
                [data-testid="stAppViewContainer"] > .main {{
                background-size: 180%;
                background-position: top left;
                background-repeat: no-repeat;
                background-attachment: local;
                }}

                [data-testid="stSidebar"] > div:first-child {{
                background-image: url("https://images.unsplash.com/photo-1557682250-33bd709cbe85?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=829&q=80");
                background-position: top left; 
                background-repeat: no-repeat;
                background-attachment: fixed;
                background-size:cover;
                }}

                [data-testid="stHeader"] {{
                background: rgba(0,0,0,0);
                }}

                [data-testid="stToolbar"] {{
                right: 2rem;
                }}
                </style>
                """

    st.markdown(page_bg_img, unsafe_allow_html=True)

def first_page(name, tipo_acesso):
    if tipo_acesso == 'Master':
        with st.sidebar:
            st.markdown("""
            <style>
                [data-testid=stSidebar] {
                    background-color: """+azul_b+""";
                }
            </style>
            """, unsafe_allow_html=True)
            st.markdown(f"""<h3 style="color: #ffffff">Bem Vindo: {name}</h3>""",unsafe_allow_html=True)

            st.image("./img/LOGO.png", width=200, use_column_width=None)
            add_select = option_menu(None,
                                    ["OKR - Geral", "OKR - Diretorias"],
                                    icons=['crosshair', 'diagram-3'],
                                    menu_icon="box",
                                    default_index=0,
                                    styles={
                                            "container": {"padding": "0!important", "background-color": "rgba(0,0,255,0.35)", "border-radius":"0.0rem"},
                                            "icon": {"color": laranja, "font-size": "20px"},
                                            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "00px","border-radius":"0.0rem",
                                                        "--hover-color": azul, "color":'white',
                                                            "padding-top": "0.6rem", "padding-bottom": "0.6rem"}, 
                                            "nav-link-selected": {"background-color": azul_b},
                                            "sidebar": {"background-color": "rgba(0,0,0,0)"},
                                        }
                                        )
            
        hide_streamlit_style = """
                        <style>
                        #MainMenu {visibility: Show;}
                        footer {visibility: hidden;}
                        </style>
                        """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        img_to_sidebar()
        return add_select
    else:
        with st.sidebar:
            st.markdown("""
            <style>
                [data-testid=stSidebar] {
                    background-color: """+azul_b+""";
                }
            </style>
            """, unsafe_allow_html=True)
            st.markdown(f"""<h3 style="color: #ffffff">Bem Vindo: {name}</h3>""",unsafe_allow_html=True)

            st.image("./img/LOGO.png", width=200, use_column_width=None)
            add_select = option_menu(None,
                                    ["OKR - Diretorias"],
                                    icons=['diagram-3'],
                                    menu_icon="box",
                                    default_index=0,
                                    styles={
                                            "container": {"padding": "0!important", "background-color": "rgba(0,0,255,0.35)", "border-radius":"0.0rem"},
                                            "icon": {"color": laranja, "font-size": "20px"},
                                            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "00px","border-radius":"0.0rem",
                                                        "--hover-color": azul, "color":'white',
                                                            "padding-top": "0.6rem", "padding-bottom": "0.6rem"}, 
                                            "nav-link-selected": {"background-color": azul_b},
                                            "sidebar": {"background-color": "rgba(0,0,0,0)"},
                                        }
                                        )
            
        hide_streamlit_style = """
                        <style>
                        #MainMenu {visibility: Show;}
                        footer {visibility: hidden;}
                        </style>
                        """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        img_to_sidebar()
        return add_select
    
@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache_data()
def get_img_with_href(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}">
            <img src="data:image/{img_format}; base64,{bin_str}"style="width:100%; height:100%" />
        </a>'''
    return html_code

def cabecalho(titulo = 'Gerenciamento do território', subTitulo = '*Projeto de Desocupação da Faixa de Domínio das Rodovias Federais BR-101/RJ-SP e BR-116/RJ-SP*'):
    col1, col2 = st.columns([1,0.2])
    with col1:
        st.title(titulo)
        st.markdown(subTitulo)

    with col2:
        gif_html = get_img_with_href('./img/NMC.png', 'https://nmcintegrativa.com.br')
        st.markdown(gif_html, unsafe_allow_html=True)
    
if __name__ == '__main__':
    # Modo tela completa
    st.set_page_config(layout="wide",page_title='Dashboard', page_icon='./img/LOGO2.png')

    if "config" not in st.session_state:
        with open('config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)
            authenticator = Authenticate(
                                        config['credentials'],
                                        config['cookie']['name'],
                                        config['cookie']['key'],
                                        config['cookie']['expiry_days'],
                                        config['preauthorized']
                                        )
            name, authentication_status, username = authenticator.login('Login', 'main')

            if authentication_status:
                authenticator.logout('Logout', 'sidebar')

                # Definir páginas de acesso
                dic_df = zf.ajustes_api()
                tipo_acesso = setup.nvl_acesso_app[name]
                
                if any(elem in name for elem in setup.usuarios_master):
                    #Adicionar layout
                    add_select = first_page(name, tipo_acesso='Master')

                    if add_select=="OKR - Geral":
                        cabecalho(titulo = 'OKR - Geral',
                                subTitulo = '*Visualização geral das metas da empresa*')
                        st.write("""***""")
                        pg_okr_geral.app(dic_df)
                        

                    elif add_select == "OKR - Diretorias":
                        cabecalho(titulo = 'OKR - Diretorias',
                                subTitulo = '*Metas por diretorias e individuais*')
                        st.write("""***""")
                        pg_okr_diretoria.app(dic_df, tipo_acesso)
                else:
                    #Adicionar layout
                    add_select = first_page(name, tipo_acesso='Diretor')

                    if add_select=="OKR - Geral":
                        cabecalho(titulo = 'OKR - Geral',
                                subTitulo = '*Visualização geral das metas da empresa*')
                        st.write("""***""")
                        pg_okr_geral.app(dic_df)
                        

                    elif add_select == "OKR - Diretorias":
                        cabecalho(titulo = 'OKR - Diretorias',
                                subTitulo = '*Metas por diretorias e individuais*')
                        st.write("""***""")
                        pg_okr_diretoria.app(dic_df, tipo_acesso)

            elif authentication_status == False:
                st.error('Usuário/senha incorreto')
            elif authentication_status == None:
                st.warning('Por favor, digite seu usuário e senha')
