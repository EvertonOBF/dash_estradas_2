from pathlib import Path
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
from utilidades import leitura_de_dados, criar_container_estilizado, criar_container_estilizado2


# ------------------------- Configurando a página -----------------------------------
st.set_page_config(
    page_title="Sub-Projeto 01 Cientista Chefe",
    page_icon="chart_with_upwards_trend",
    layout="wide")

# Removendo o recuo do texto superior
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

# -------------------------------- Leitura dos dados -----------------------------
########### Leitura dos dados
leitura_de_dados()
df_FWD = st.session_state['dados']['df_FWD']
df_IRI = st.session_state['dados']['df_IRI']
df_coord = st.session_state['dados']['df_coor']

# -------------------------------- Título do dash -------------------------------------
st.markdown("""
    <style>
    .big-font {
        font-size:25px !important;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Usar a classe CSS para configurar o tamanho da fonte
st.markdown(
    """
    <h2 class="big-font" style="margin-bottom: 1em;">
        Análise das condições funcionais e estruturais em obras rodoviárias do Ceará <br>Controle de Qualidade
    </h2>
    """,
    unsafe_allow_html=True
)
## -------------------------- Variáveis monitoradas --------------------------------------

# -------------------------- Cards ------------------------------------------------------
card1, card2, card3, card4, card5   = st.columns(5)

# Total de rodovias monitoradas
total_rodovias = len(df_FWD['VIA'].unique())

with card1:
    criar_container_estilizado2('Rodovias Monitoradas', total_rodovias)

# Total de Quilômetros monitorados
with card2:
    xx = df_FWD.groupby(['VIA','DIRECAO'])['ESTACA'].max().reset_index().rename(columns={'ESTACA':'Fim'})
    yy = df_FWD.groupby(['VIA','DIRECAO'])['ESTACA'].min().reset_index().rename(columns={'ESTACA':'Inicio'})
    extensao = xx.merge(yy, left_on=['VIA', 'DIRECAO'], right_on=['VIA', 'DIRECAO'])
    extensao['Extensao'] = extensao['Fim'] - extensao['Inicio']
    total_extensao = (extensao['Extensao'].sum())
    criar_container_estilizado2('Quilômetros Monitorados', f"{round(total_extensao/1000,2)} km")


# Número total de medições realizadas em campo
with card3:
    total_medicoes = df_FWD.shape[0] + df_IRI.shape[0]
    criar_container_estilizado2('Medições Realizadas', total_medicoes)

with card4:
    iri_media = df_IRI['VARIAVEL'].mean()
    iri_cv = (df_IRI['VARIAVEL'].std()/iri_media)*100
    criar_container_estilizado('IRI', round(iri_media,2), round(iri_cv,2))

with card5:
    fwd_media = df_FWD['VARIAVEL'].mean()
    fwd_cv = (df_FWD['VARIAVEL'].std()/fwd_media)*100
    criar_container_estilizado('FWD', round(fwd_media,2), round(fwd_cv,2))

style_metric_cards()

# ------------------------- Gráficos Gerais ------------------------------------------
tab1, tab2, tab3 = st.tabs(["Condições das Rodovias", "Total de Medições por Rodovia", "Extensão de Monitoramento por Rodovia"])


with tab1:
    cond = df_IRI.groupby('CONDICAO')['ENSAIO'].size().reset_index().rename(columns={'ENSAIO':'Total', 'CONDICAO':'Condição'})
    cores = {'ÓTIMO': 'mediumblue','BOM': 'yellowgreen','REGULAR': 'yellow', 'RUIM': 'orangered','PÉSSIMO': 'firebrick'}

    fig = px.pie(cond, values='Total', names='Condição', hole=.3, color='Condição',
                     color_discrete_map=cores,
                     labels={'Total': "Trechos", "Condição": "Classificação:"},
                     category_orders={"Condição": ['ÓTIMO', 'BOM', 'REGULAR', 'RUIM', 'PÉSSIMO']})
    
    fig.update_layout({'margin':{'l':0, 'r':10 , 't':50, 'b':0}}, height=350)
    fig.update_traces(textfont_size=15,marker=dict(line=dict(color='#000000', width=1)))
    st.plotly_chart(fig, config=config)

with tab2:
    # Número de medições por rodovia
    medicoes_FWD = df_FWD.groupby(['VIA'])['ESTACA'].size().reset_index().rename(columns={'ESTACA':'Total - FWD'})
    medicoes_iri = df_IRI.groupby(['VIA'])['ESTACA'].size().reset_index().rename(columns={'ESTACA':'Total - iri'})
    medicoes_estrada =  medicoes_FWD.merge(medicoes_iri, left_on='VIA', right_on='VIA')
    medicoes_estrada['Total'] = medicoes_FWD['Total - FWD'] + medicoes_iri['Total - iri']
    medicoes_estrada = medicoes_estrada.sort_values(by='Total', ascending=False)

    #medicoes_estrada
    fig = px.bar(medicoes_estrada, x='VIA', y = 'Total')
    fig.update_layout({'margin':{'l':0, 'r':10 , 't':10, 'b':0}}, height=400)
    fig.update_xaxes(title='Rodovia', linewidth=1, linecolor='black')
    fig.update_yaxes(title='Número de Medições', linewidth=1, linecolor='black')
    st.plotly_chart(fig, config=config)

with tab3:
    # Quilometros analisados por rodovia
    tamanho_rodovia = extensao.groupby('VIA')['Extensao'].sum().reset_index().sort_values(by="Extensao", ascending=False)
    tamanho_rodovia['Extensao'] = tamanho_rodovia['Extensao']/1000
    fig = px.bar(tamanho_rodovia, x='VIA', y = 'Extensao')
    fig.update_layout({'margin':{'l':0, 'r':10 , 't':10, 'b':0}}, height=400)
    fig.update_xaxes(title='Rodovia', linewidth=1, linecolor='black')
    fig.update_yaxes(title='Extensão (km)', linewidth=1, linecolor='black')
    st.plotly_chart(fig, config=config)

