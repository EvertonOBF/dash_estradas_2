from pathlib import Path
import streamlit as st
import plotly.express as px
import pandas as pd

from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
from utilidades import leitura_de_dados
import folium
from streamlit_folium import folium_static
from branca.colormap import LinearColormap

st.set_page_config(
    page_title="Sub-Projeto 01 Cientista Chefe",
    page_icon="chart_with_upwards_trend",
    layout="wide")

# -------------------------- Removendo o recuo do texto superior -------------------------------
st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 2rem;
                    padding-right: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)

config = {'displayModeBar': False}

#------------------------------ Leitura dos dados ------------------------------------
leitura_de_dados()
df_FWD = st.session_state['dados']['df_FWD']
df_IRI = st.session_state['dados']['df_IRI']
df_coord = st.session_state['dados']['df_coor']
df_coord2 = st.session_state['dados']['df_coor2']

#------------------------ sidebar ---------------------------------------------------

bar= st.sidebar

infor = bar.selectbox(
    "Tipo de Análise:",
    ["IRI", "FWD"])

#########
via = bar.selectbox(
    "Rodovia de interesse:",
    df_FWD.VIA.unique())
#########
sent = bar.selectbox(
    "Sentido da via:",
    df_FWD.DIRECAO.unique())

df_FWD_ger = df_FWD[(df_FWD["VIA"] == via) & (df_FWD["DIRECAO"] == sent)]
df_IRI_ger = df_IRI[(df_IRI["VIA"] == via) & (df_IRI["DIRECAO"] == sent)]

st.markdown(f'##### {infor} - Rodovia: {via} - Trecho: {sent}')

# -------------------------------------- Criando as fíguras -----------------------------------------

def gerar_figura_01():
    fig1 = px.bar(df_FWD_ger, x="PONTO", y="VARIAVEL",color="TRAFEGO",
                      category_orders={"TRAFEGO": ['TRÁFEGO LEVE','TRÁFEGO MÉDIO','TRÁFEGO MEIO PESADO','TRÁFEGO PESADO']},
                      color_discrete_sequence=["firebrick", "orangered", "yellowgreen", "mediumblue"],
                      labels={'PONTO': '','VARIAVEL': 'Deflexão (0,01mm)'})
    
    fig1.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="left", x=0), width=650, height=390)
    
    return fig1

def gerar_figura_02():
    fig2 = px.pie(df_FWD_ger, values="PIE", names="CONDICAO", hole=.3,color="CONDICAO",
                      color_discrete_map={'ACEITO':"mediumblue",'ATENÇÃO':"yellowgreen",'FISSURAÇÃO PRECOCE':"orangered",'REJEIÇÃO':"firebrick"},
                      labels={'PIE':"Contagem", "CONDICAO":"Classificação:"},
                      category_orders={"CONDICAO": ['ACEITO', 'ATENÇÃO', 'FISSURAÇÃO PRECOCE', 'REJEIÇÃO']},
                      )
                      
    fig2.update_traces(textfont_size=15, marker=dict(line=dict(color='#000000', width=1)))
    fig2.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="left", x=0), width=320, height=390)
    return fig2

def gerar_figura_03():
    fig3 = px.scatter(df_IRI_ger, x="DIST", y="VARIAVEL", color="CONDICAO",symbol = "OBS",
                          labels={'DIST': 'Distância (km)','VARIAVEL': 'Índice de Irregularidade Internacional (IRI)', "CONDICAO": "Classificação", "OBS":""},
                          color_discrete_map={'ÓTIMO': 'mediumblue',
                                              'BOM': 'yellowgreen',
                                              'REGULAR': 'yellow',
                                              'RUIM': 'orangered',
                                              'PÉSSIMO': 'firebrick'},

                          )
    fig3.add_hline(y=2.0, line_color='mediumblue', line_dash="dash", annotation_text='LIMITE ÓTIMO E BOM',annotation_position="bottom right", annotation_font_color="black")#,annotation_font_size=24,)
    fig3.add_hline(y=2.7, line_color='yellowgreen', line_dash="dash", annotation_text='LIMITE BOM E REGULAR', annotation_position="bottom right", annotation_font_color="black")#,annotation_font_size=24,annotation_font_color="black")
    fig3.add_hline(y=3.5, line_color='yellow', line_dash="dash", annotation_text='LIMITE REGULAR E RUIM', annotation_position="bottom right", annotation_font_color="black")#,annotation_font_size=24,annotation_font_color="black")
    fig3.add_hline(y=5.5, line_color='orangered', line_dash="dash", annotation_text='LIMITE RUIM E PÉSSIMO', annotation_position="bottom right", annotation_font_color="black")#,annotation_font_size=24,annotation_font_color="black")
    fig3.update_layout({'margin':{'l':0, 'r':10 , 't':10, 'b':0}}, showlegend=False, width=650, height=390)
    return fig3

def gerar_figura_04():
    fig4 = px.pie(df_IRI_ger, values='PIE', names='CONDICAO', hole=.3, color='CONDICAO',
                     color_discrete_map={'ÓTIMO': 'mediumblue',
                                         'BOM': 'yellowgreen',
                                         'REGULAR': 'yellow',
                                         'RUIM': 'orangered',
                                         'PÉSSIMO': 'firebrick'},
                     labels={'PIE': "Contagem", "CONDICAO": "Classificação:"},
                     category_orders={"CONDICAO": ['ÓTIMO', 'BOM', 'REGULAR', 'RUIM', 'PÉSSIMO']})
    
    fig4.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="left", x=0.01), width=320)

    fig4.update_traces(textfont_size=15,marker=dict(line=dict(color='#000000', width=1)))
    return fig4

# ----------------------------- MAPA -------------------------------------------------------------------

def mostra_mapa(via):
    df1 = df_coord2[df_coord2['VIA'] == via].copy()

    df = df1[df1['VIA'] == via].copy()

    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=11, width='100%', height='410px')#, tiles="cartodb positron")

    # Definir manualmente 6 cores
    #custom_colors = ["#00FF00", "#7FFF00", "#FFFF00", "#FFBF00", "#FF8000", "#FF0000"]
    custom_colors = ["#1a9850", "#91cf60", "#d9ef8b", "#fee08b", "#fc8d59", "#d73027"]
    
    df.loc[:, 'color_bin'] = pd.cut(df['VARIAVEL'], bins=len(custom_colors), labels=custom_colors)

    # Configurar o LinearColormap com as cores manuais
    linear_colormap = LinearColormap(
        colors=custom_colors,
        vmin=df['VARIAVEL'].min(),
        vmax=df['VARIAVEL'].max(),
        caption="Escala de Valores FWD"
    )

    # Adicionar o LinearColormap ao mapa
    linear_colormap.add_to(m)  # Somente essa barra será adicionada

    # Adicionar os pontos ao mapa com cores personalizadas
    for idx, row in df.iterrows():
        color = row['color_bin']  # Cor definida pela categorização
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=2,  # Tamanho do círculo
            color=color,  # Cor do círculo
            fill=True,
            fill_opacity=0.6,
            fill_color=color,  # Cor de preenchimento
            popup=f"Ponto: {row['PONTO']}, Var: {row['VARIAVEL']}"
        ).add_to(m)

    # Exibir o mapa
    folium_static(m)

# --------------------------------------- Cálculo das métricas ---------------------------------------

# Número de medições:
total_medidas_IRI = df_IRI_ger.shape[0]
total_medidas_FWD = df_FWD_ger.shape[0]

# Espaçamento entre medições:
esp_fwd = '1 km'
esp_IRI = '-'

# Média
avg_VAR_FWD = df_FWD_ger["VARIAVEL"].mean()
avg_VAR_IRI = df_IRI_ger["VARIAVEL"].mean()

# Mediana
med_VAR_FWD = df_FWD_ger["VARIAVEL"].median()
med_VAR_IRI = df_IRI_ger["VARIAVEL"].median()

# Desvio padrão
std_VAR_FWD = df_FWD_ger["VARIAVEL"].std()
std_VAR_IRI = df_IRI_ger["VARIAVEL"].std()

# Coeficiente de variação
cv_VAR_FWD = (std_VAR_FWD/avg_VAR_FWD)*100
cv_VAR_IRI = (std_VAR_IRI/avg_VAR_IRI)*100
#########

st.markdown(f'##### {infor} - Rodovia: {via} - Trecho: {sent}')
#st.markdown(f"##### {via} — {sent}")

kpi1, kpi2, kpi3, kpi4, kpi5  = st.columns(5)

if infor == "FWD":
    kpi1.metric(label="Média", value=round(avg_VAR_FWD,2))
    #kpi2.metric(label="Mediana 📈", value=round(med_VAR_FWD, 2))
    kpi2.metric(label="Desvio Padrão", value=round(std_VAR_FWD,2))
    kpi3.metric(label="Coeficiente de Variação", value=f"{round(cv_VAR_FWD,2)} %")
    kpi4.metric(label="Total de Medições", value=f"{total_medidas_FWD}")
    kpi5.metric(label="Espaçamento entre medições", value=f"{esp_fwd}")
    #kpi6.metric(label=" 📈", value=f"{total_medidas_FWD}")
    
    style_metric_cards()

elif infor == "IRI":
    kpi1.metric(label="Média", value=round(avg_VAR_IRI,2))
    #kpi2.metric(label="Mediana 📈", value=round(med_VAR_IRI, 2))
    kpi2.metric(label="Desvio Padrão", value=round(std_VAR_IRI,2))
    kpi3.metric(label="Coeficiente de Variação", value=f"{round(cv_VAR_IRI,2)} %")
    kpi4.metric(label="Total de Medições", value=f"{total_medidas_IRI}")
    kpi5.metric(label="Espaçamento entre medições", value=f"{esp_IRI}")
    
    style_metric_cards()

col1, col2 = st.columns([3, 2], gap="medium")

if infor == "FWD":
    tab1, tab2 = st.tabs(["Figuras", "Tabela"])

    with tab1:
        col1, col2 = st.columns([3, 2], gap="medium")
        
        with col1:
            st.markdown("###### Deflexão (0,01 mm) por trecho da rodovia")
            fig1 = gerar_figura_01()
            st.plotly_chart(fig1, config=config)

        with col2:
            st.markdown("###### Percentual por Classificação da Condição do Pavimento")
            fig2 = gerar_figura_02()
            st.plotly_chart(fig2, config=config)
            st.markdown(
                "<style> .stDeck {align-items: center;} .st-jeLOwI {margin-left: -50px;}</style>", 
                unsafe_allow_html=True
            )
        
    with tab2:
        mostra_mapa(via)
        #st.dataframe(df_FWD)

elif infor == "IRI":
    tab1, tab2 = st.tabs(["Figuras", "Tabela"])
    
    with tab1:
        col1, col2 = st.columns([3, 2], gap="medium")
        
        with col1:
            st.markdown("###### Distribuição do IRI na via")
            fig3 = gerar_figura_03()
            st.plotly_chart(fig3, config=config)
        
        with col2:
            st.markdown("###### Percentual por Classificação do IRI")
            fig4 = gerar_figura_04()
            st.plotly_chart(fig4, config=config)
    
    with tab2:
        mostra_mapa(via)