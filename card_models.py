
import streamlit as st
import base64
import re

# Cores NMC
roxo = "#521C78"
laranja = "#F0A800"
azul = "#121C4D"
azul_b = "#14A2dc"
vermelho = "#E8501C"
verde = "#198036"
amarelo = "#DDD326"
paleta_IVS = [azul_b, azul, amarelo, laranja, vermelho]
paleta_NMC = [roxo, laranja, azul, vermelho, azul_b, verde, amarelo]

def card_simple(titulo_box, valor_box, cor_caixa='#7ED1EF', cor_font='white', fontsize=50,
                  iconname="fa-solid fa-venus"):
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


def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")

def card_equipe(img, nome, descricao):
    img = get_img_as_base64(img)
    html = f"""
            <div class="container">
            <section class="mx-auto my-5" style="max-width: 23rem;">
                <div class="card testimonial-card mt-2 mb-3">
                <div class="card-up aqua-gradient"></div>
                <div class="avatar mx-auto white">
                    <img src= "data:image/gif;base64,{img}" class="rounded-circle img-fluid"
                    alt="">
                </div>
                <div class="card-body text-center">
                    <h3 class="card-title font-weight-bold">{nome}</h3>
                    <hr margin:0rem 0px></hr>
                    <p><i class="fas fa-quote-left"></i>{descricao}</p>
                </div>
                </div>
            </section>
            </div>
            """
    
    st.markdown(html, unsafe_allow_html=True)
    with open('style_card.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def progress_bar(val, cor):
    html = f"""
                <div class="progress mt-0 mb-0" style="height: 28px;">
                    <div class="progress-bar" role="progressbar" style="width: {val}%; background-color: {cor}; font-size:22px" aria-valuenow="{val}" aria-valuemin="0" aria-valuemax="100">{val}%</div>
                </div><br>
                """
    st.markdown(html, unsafe_allow_html=True)

def card_progress(val,val_meta, titulo, icon, cor):
    
    html = f"""
            <link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
            <link rel="stylesheet" type="text/css" href="https://pixinvent.com/stack-responsive-bootstrap-4-admin-template/app-assets/css/bootstrap-extended.min.css">
            <link rel="stylesheet" href="https://use.fontawesome.com/releases/v6.3.0/css/all.css" crossorigin="anonymous">
            <link rel="stylesheet" type="text/css" href="https://pixinvent.com/stack-responsive-bootstrap-4-admin-template/app-assets/css/colors.min.css">
            <link rel="stylesheet" type="text/css" href="https://pixinvent.com/stack-responsive-bootstrap-4-admin-template/app-assets/css/bootstrap.min.css">
            <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap" rel="stylesheet">
            <div class="card">
                    <div class="card-content">
                        <div class="card-body">
                        <div class="media d-flex">
                            <div class="media-body text-left">
                            <h1 class="val" style="color: {cor}">{val_meta}</h1>
                              <span style="font-size:19px">{titulo}</span>
                              </div>
                                <div class="align-self-center">
                                <i class="{icon}  font-large-3 float-left" style="color: {cor}"></i>
                                </div>
                        </div>
                        <div class="progress mt-1 mb-0" style="height: 25px;">
                            <div class="progress-bar" role="progressbar" style="width: {val}%; background-color: {cor}; font-size:17px" aria-valuenow="{val}" aria-valuemin="0" aria-valuemax="100">{val}%</div>
                        </div>
                        </div>
                    </div>
                    </div>
                """
    st.markdown(html, unsafe_allow_html=True)

def card_metric(icon, valor, descricao, variacao, cor_icon):
    val = int(re.findall(r'(\d+)', valor)[0])
    vari = int(re.findall(r'(\d+)', variacao)[0])
    if val>0:
        cor = '#4CA780'
    else:
        cor = vermelho

    if vari>0:
        cor_vari = '#4CA780'
        sentido='up'
        icon_arrow = f"fa-solid fa-caret-{sentido}"
    elif vari<0:
        cor_vari = vermelho
        sentido ='down'
        icon_arrow = f"fa-solid fa-caret-{sentido}"
    else:
        cor_vari = azul_b
        icon_arrow = ""

    html = f"""
        <link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
        <link rel="stylesheet" type="text/css" href="https://pixinvent.com/stack-responsive-bootstrap-4-admin-template/app-assets/css/bootstrap-extended.min.css">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v6.3.0/css/all.css" crossorigin="anonymous">
        <link rel="stylesheet" type="text/css" href="https://pixinvent.com/stack-responsive-bootstrap-4-admin-template/app-assets/css/colors.min.css">
        <link rel="stylesheet" type="text/css" href="https://pixinvent.com/stack-responsive-bootstrap-4-admin-template/app-assets/css/bootstrap.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap" rel="stylesheet">
        <div class="card">
          <div class="card-content">
            <div class="card-body">
              <div class="media d-flex">
                <div class="align-self-center">
                  <i class="{icon}  font-large-3 float-left" style="color: {cor_icon};"></i>
                </div>
                <div class="media-body text-right">
                  <h1 class="card-val" style="color: {cor_icon}""> {valor}</h1>
                  <span class="text mr-9" style="color: {cor_vari};font-size:18.0pt;"><i class="{icon_arrow}" style="color: {cor_vari};"></i><b>{variacao}</b></span>
                  <span class="card-descri" style="color: #363636"">{descricao}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        """
    st.markdown(html, unsafe_allow_html=True)

def card_info(icon, cor, valor, descricao):
    html = f"""
        <link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
        <link rel="stylesheet" type="text/css" href="https://pixinvent.com/stack-responsive-bootstrap-4-admin-template/app-assets/css/bootstrap-extended.min.css">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v6.3.0/css/all.css" crossorigin="anonymous">
        <link rel="stylesheet" type="text/css" href="https://pixinvent.com/stack-responsive-bootstrap-4-admin-template/app-assets/css/colors.min.css">
        <link rel="stylesheet" type="text/css" href="https://pixinvent.com/stack-responsive-bootstrap-4-admin-template/app-assets/css/bootstrap.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap" rel="stylesheet">
        <div class="card">
          <div class="card-content">
            <div class="card-body">
              <div class="media d-flex">
                <div class="align-self-center">
                  <i class="{icon}  font-large-4 float-left" style="color: {cor};"></i>
                </div>
                <div class="media-body text-right">
                  <h1 class="card-val" style="color: {cor}"> {valor}</h1>
                  <span class="card-descri" style="font-size:19px" style="color: #363636"">{descricao}</span>
                  <h6></h6>
                </div>
              </div>
            </div>
          </div>
        </div>
        """
    st.markdown(html, unsafe_allow_html=True)


def card_metric_test():
    html = """<link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet">
          <div class="container">
              <div class="row">
                  <div class="col-md-4 col-xl-3">
                      <div class="card bg-c-blue order-card">
                          <div class="card-block">
                              <h6 class="m-b-20">Orders Received</h6>
                              <h2 class="text-right"><i class="fa fa-cart-plus f-left"></i><span>486</span></h2>
                              <p class="m-b-0">Completed Orders<span class="f-right">351</span></p>
                          </div>
                      </div>
                  </div>
                  <div class="col-md-4 col-xl-3">
                      <div class="card bg-c-green order-card">
                          <div class="card-block">
                              <h6 class="m-b-20">Orders Received</h6>
                              <h2 class="text-right"><i class="fa fa-rocket f-left"></i><span>486</span></h2>
                              <p class="m-b-0">Completed Orders<span class="f-right">351</span></p>
                          </div>
                      </div>
                  </div>
                  <div class="col-md-4 col-xl-3">
                      <div class="card bg-c-yellow order-card">
                          <div class="card-block">
                              <h6 class="m-b-20">Orders Received</h6>
                              <h2 class="text-right"><i class="fa fa-refresh f-left"></i><span>486</span></h2>
                              <p class="m-b-0">Completed Orders<span class="f-right">351</span></p>
                          </div>
                      </div>
                  </div>
                  <div class="col-md-4 col-xl-3">
                      <div class="card bg-c-pink order-card">
                          <div class="card-block">
                              <h6 class="m-b-20">Orders Received</h6>
                              <h2 class="text-right"><i class="fa fa-credit-card f-left"></i><span>486</span></h2>
                              <p class="m-b-0">Completed Orders<span class="f-right">351</span></p>
                          </div>
                      </div>
                  </div>
            </div>
          </div>"""
    st.markdown(html, unsafe_allow_html=True)

    css = """
              body{
                  margin-top:20px;
                  background:#FAFAFA;
              }
              .order-card {
                  color: #fff;
              }
              .bg-c-blue {
                  background: linear-gradient(45deg,#4099ff,#73b4ff);
              }
              .bg-c-green {
                  background: linear-gradient(45deg,#2ed8b6,#59e0c5);
              }
              .bg-c-yellow {
                  background: linear-gradient(45deg,#FFB64D,#ffcb80);
              }
              .bg-c-pink {
                  background: linear-gradient(45deg,#FF5370,#ff869a);
              }
              .card {
                  border-radius: 5px;
                  -webkit-box-shadow: 0 1px 2.94px 0.06px rgba(4,26,55,0.16);
                  box-shadow: 0 1px 2.94px 0.06px rgba(4,26,55,0.16);
                  border: none;
                  margin-bottom: 30px;
                  -webkit-transition: all 0.3s ease-in-out;
                  transition: all 0.3s ease-in-out;
              }
              .card .card-block {
                  padding: 25px;
              }
              .order-card i {
                  font-size: 26px;
              }
              .f-left {
                  float: left;
              }
              .f-right {
                  float: right;
              }
    """
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

def progressBarCircle(val1, val2, val3, pct1, pct2, pct3, texto1, texto2, texto3, cor1, cor2, cor3):
    import numpy as np
    if pct1 == 0 and pct2!=0 and pct3!=0:
        raio1=1
        raio2 = (125.6*2)/(100/pct2)
        raio3 = (125.6*2)/(100/pct3)
    elif pct2 == 0 and pct1!=0 and pct3!=0:
        raio2=1
        raio1 = (125.6*2)/(100/pct1)
        raio3 = (125.6*2)/(100/pct3)
    elif pct3 == 0 and pct1!=0 and pct2!=0:
        raio3=1
        raio1 = (125.6*2)/(100/pct1)
        raio2 = (125.6*2)/(100/pct2)
    elif pct2==0 and pct1==0 and pct3==0:
        raio1=1
        raio2=1
        raio3=1
    else:
        try:
            raio1 = (125.6*2)/(100/pct1)
        except:
            raio1 = 1
        try:
            raio2 = (125.6*2)/(100/pct2)
        except:
            raio2 = 1
        try:
            raio3 = (125.6*2)/(100/pct3)
        except:
            raio3 = 1
    px = '180px'

    html = f"""
          <svg id="svg" viewbox="0 0 125 100" width="{px}" height="{px}">
            <circle cx="50" cy="50" r="45" fill="{cor1}"/>
            <path fill="none" stroke-linecap="round" stroke-width="5" stroke="#fff"
                  stroke-dasharray="{raio1}, 300"
                  d="M50 10
                    a 40 40 0 0 1 0 80
                    a 40 40 0 0 1 0 -80"/>
            <text x="50" y="50" text-anchor="middle" dy="7" font-size="23">{val1}</text>
            <text x="50" y="60" text-anchor="middle" dy="7" font-size="12">{texto1}</text>
          </svg>
          <svg id="svg" viewbox="0 0 125 100" width="{px}" height="{px}">
            <circle cx="50" cy="50" r="45" fill="{cor2}"/>
            <path fill="none" stroke-linecap="round" stroke-width="5" stroke="#fff"
                  stroke-dasharray="{raio2}, 300"
                  d="M50 10
                    a 40 40 0 0 1 0 80
                    a 40 40 0 0 1 0 -80"/>
            <text x="50" y="50" text-anchor="middle" dy="7" font-size="23">{val2}</text>
            <text x="50" y="60" text-anchor="middle" dy="7" font-size="12">{texto2}</text>
          </svg>
          <svg id="svg" viewbox="0 0 125 100" width="{px}" height="{px}">
            <circle cx="50" cy="50" r="45" fill="#754993"/>
            <path fill="none" stroke-linecap="round" stroke-width="5" stroke="#fff"
                  stroke-dasharray="{raio3}, 300"
                  d="M50 10
                    a 40 40 0 0 1 0 80
                    a 40 40 0 0 1 0 -80"/>
            <text x="50" y="50" text-anchor="middle" dy="7" font-size="23">{val3}</text>
            <text x="50" y="60" text-anchor="middle" dy="7" font-size="12">{texto3}</text>
          </svg>
          """
    st.markdown(html, unsafe_allow_html=True)

def progressBarCircle2(val1, val2, val3, pct1, pct2, pct3, texto1, texto2, texto3, cor1, cor2, cor3):
    import numpy as np
    if pct1 == 0 and pct2!=0 and pct3!=0:
        raio1=1
        raio2 = (125.6*2)/(100/pct2)
        raio3 = (125.6*2)/(100/pct3)
    elif pct2 == 0 and pct1!=0 and pct3!=0:
        raio2=1
        raio1 = (125.6*2)/(100/pct1)
        raio3 = (125.6*2)/(100/pct3)
    elif pct3 == 0 and pct1!=0 and pct2!=0:
        raio3=1
        raio1 = (125.6*2)/(100/pct1)
        raio2 = (125.6*2)/(100/pct2)
    elif pct2==0 and pct1==0 and pct3==0:
        raio1=1
        raio2=1
        raio3=1
    else:
        try:
            raio1 = (125.6*2)/(100/pct1)
        except:
            raio1 = 1
        try:
            raio2 = (125.6*2)/(100/pct2)
        except:
            raio2 = 1
        try:
            raio3 = (125.6*2)/(100/pct3)
        except:
            raio3 = 1
    px = '180px'

    html = f"""
          <svg id="svg" viewbox="0 0 125 100" width="{px}" height="{px}">
            <circle cx="50" cy="50" r="45" fill="#754993"/>
            <path fill="none" stroke-linecap="round" stroke-width="5" stroke="#fff"
                  stroke-dasharray="{raio3}, 300"
                  d="M50 10
                    a 40 40 0 0 1 0 80
                    a 40 40 0 0 1 0 -80"/>
            <text x="50" y="50" text-anchor="middle" dy="7" font-size="23">{val3}</text>
            <text x="50" y="60" text-anchor="middle" dy="7" font-size="12">{texto3}</text>
          </svg>
          <svg id="svg" viewbox="0 0 125 100" width="{px}" height="{px}">
            <circle cx="50" cy="50" r="45" fill="{cor2}"/>
            <path fill="none" stroke-linecap="round" stroke-width="5" stroke="#fff"
                  stroke-dasharray="{raio2}, 300"
                  d="M50 10
                    a 40 40 0 0 1 0 80
                    a 40 40 0 0 1 0 -80"/>
            <text x="50" y="50" text-anchor="middle" dy="7" font-size="23">{val2}</text>
            <text x="50" y="60" text-anchor="middle" dy="7" font-size="12">{texto2}</text>
          </svg>
          """
    st.markdown(html, unsafe_allow_html=True)


def progressBarOnly():
      
      html = f"""<div class="container">
          <div class="row">
              <div class="col-md-6">
                  <h3 class="progress-title">Faturamento - 60%</h3>
                  <div class="progress red">
                      <div class="progress-bar" style="width:60%; background:#ef5b5b;"></div>
                  </div>
                  <h3 class="progress-title">Lucro - 10%</h3>
                  <div class="progress yellow">
                      <div class="progress-bar" style="width:90%; background:#ffc116;"></div>
                  </div>
              </div>
          </div>
      </div>"""
      st.markdown(html, unsafe_allow_html=True)

      css = """
            .progress-title{
                font-size: 18px;
                font-weight: 700;
                font-style: italic;
                color: #455493;
                margin: 0 0 20px;
            }
            .progress{
                height: 7px;
                background: #f8f8f8;
                border-radius: 0;
                box-shadow: none;
                margin-bottom: 30px;
                overflow: visible;
            }
            .progress .progress-bar{
                box-shadow: none;
                border-radius: 0;
                position: relative;
                -webkit-animation: animate-positive 2s;
                animation: animate-positive 2s;
            }
            .progress .progress-bar:before,
            .progress .progress-bar:after{
                content: "";
                width: 20px;
                height: 20px;
                background: #fff;
                position: absolute;
                top: -6px;
                right: 16px;
                transform: rotate(45deg);
            }
            .progress .progress-bar:after{
                border: 4px solid #fff;
                position: absolute;
                right: 2px;
            }
            .progress.red .progress-bar:before,
            .progress.red .progress-bar:after{
                outline: 14px solid #ef5b5b;
            }
            .progress.red .progress-bar:after{
                background: #ef5b5b;
            }
            .progress.yellow .progress-bar:before,
            .progress.yellow .progress-bar:after{
                outline: 4px solid #ffc116;
            }
            .progress.yellow .progress-bar:after{
                background: #ffc116;
            }
            .progress.blue .progress-bar:before,
            .progress.blue .progress-bar:after{
                outline: 4px solid #20a39e;
            }
            .progress.blue .progress-bar:after{
                background: #20a39e;
            }
            .progress.green .progress-bar:before,
            .progress.green .progress-bar:after{
                outline: 4px solid #7cb518;
            }
            .progress.green .progress-bar:after{
                background: #7cb518;
            }
            @-webkit-keyframes animate-positive{
                0%{ width: 0; }
            }
            @keyframes animate-positive{
                0%{ width: 0; }
            }
      """
      st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)