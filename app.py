import streamlit as st
from PIL import Image
from nuvem import gerar_nuvem_palavras
import json

def landing_page():
    st.title('Análise de chat')

    comments_json = st.file_uploader('Comentários em .json', type='json')

    if st.button('Iniciar análise'):
        analyze_chat(comments_json)

def analyze_chat(comments_json):
    if comments_json is not None:
        # Chama analise
        comments_file = comments_json.read()
        data = json.loads(comments_file)
        gerar_nuvem_palavras(data)
        dashboard()
    else:
        st.error('Faça o upload do arquivo de comentários')

def dashboard():
    st.image('output/nuvem_de_palavras.png')

landing_page()