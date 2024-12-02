import streamlit as st
import pandas as pd
from pathlib import Path
from streamlit_extras.stylable_container import stylable_container


def leitura_de_dados():
    if not 'dados' in st.session_state:
        pasta_datasets = Path(__file__).parents[0] / 'datasets'
        df_FWD=pd.read_excel(pasta_datasets /'BASE_DADOS_FWD.xlsx', header=0)
        df_IRI=pd.read_excel(pasta_datasets /'BASE_DADOS_IRI.xlsx', header=0, sheet_name="BASE_DADOS_TRAT")
        df_coord = pd.read_excel(pasta_datasets /'COORDENADAS_DAS_ESTACAS.xlsx')
        df_coord2 = pd.read_csv(pasta_datasets /'data_fwd.csv')

        dados = {'df_FWD': df_FWD,
                'df_IRI': df_IRI,
                'df_coor': df_coord,
                'df_coor2' : df_coord2}
    
        st.session_state['caminho_datasets'] = pasta_datasets
        st.session_state['dados'] = dados

def criar_container_estilizado(texto, media, cv):
    # Conteúdo do container com múltiplas linhas
    conteudo_container = f"""
    <div style="font-size: 1.1em; line-height: 1.05;">
        <span style="font-size: 1.05em; font-weight: bold; margin-bottom: 0.2em; display: block;">{texto}</span>
        <span style="font-size: 0.9em;">Média: {media}</span><br>
        <span style="font-size: 0.9em;">Coef. de Variação: {cv} %</span>
    </div>
    """

    # Exibir o container estilizado com borda e texto em múltiplas linhas
    with stylable_container(
        key="container_with_border",
        css_styles="""
        {
            border-top: 1px solid rgba(49, 51, 63, 0.2);
            border-right: 1px solid rgba(49, 51, 63, 0.2);
            border-bottom: 1px solid rgba(49, 51, 63, 0.2);
            border-left: 10px solid #ADD8E6; /* Largura e cor da borda esquerda */
            border-radius: 0.5rem;
            padding: calc(1em - 1px);
            padding-bottom: 2em; /* Aumenta o espaço interno na parte inferior */
            padding-top: 1.em; /* Aumenta o espaço interno na parte inferior */
        }
        """,
    ):
        return st.write(conteudo_container, unsafe_allow_html=True)

def criar_container_estilizado2(texto, valor):
    # Conteúdo do container com múltiplas linhas
    conteudo_container = f"""
    <div style="font-size: 1.7em; line-height: 1.2;">
        <span style="font-size: 0.6em; margin-bottom: 0.5em; display: block;">{texto}</span>
        <span style="font-size: 1.0em; font-weight: bold;">{valor}</span><br>
    </div>
    """

    # Exibir o container estilizado com borda e texto em múltiplas linhas
    with stylable_container(
        key="container_with_border",
        css_styles="""
        {
            border-top: 1px solid rgba(49, 51, 63, 0.2);
            border-right: 1px solid rgba(49, 51, 63, 0.2);
            border-bottom: 1px solid rgba(49, 51, 63, 0.2);
            border-left: 10px solid #ADD8E6; /* Largura e cor da borda esquerda */
            border-radius: 0.5rem;
            padding: calc(1em - 1px);
            padding-bottom: 2em; /* Aumenta o espaço interno na parte inferior */
        }
        """,
    ):
        return st.write(conteudo_container, unsafe_allow_html=True)