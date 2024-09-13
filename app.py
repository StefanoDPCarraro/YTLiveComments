import streamlit as st
from PIL import Image
from nuvem import gerar_nuvem_palavras
from stats import get_top_authors, get_author_comments

st.session_state['comments_json'] = 'comments.json'

def landing_page():
    st.title('Análise de chat')

    if st.button('Iniciar análise'):
        analyze_chat(st.session_state['comments_json'])

def analyze_chat(comments_json):
    if comments_json is not None:
        gerar_nuvem_palavras(comments_json)
    else:
        st.error('Faça o upload do arquivo de comentários')

def comments_peak():
    pass

def most_comments():
    st.title('Maiores comentaristas')
    n_authors = st.slider('Número de comentaristas', 1, 10, 5)
    if st.session_state['comments_json'] is not None:
        authors = get_top_authors(st.session_state['comments_json'], n=n_authors)
        for author, count in authors:
            with st.expander(f'{author}: {count} comentários'):
                comments = get_author_comments(author, st.session_state['comments_json'])
                for comment in comments:
                    st.write(comment)


    else:
        st.error('Faça o upload do arquivo de comentários')

def dashboard():
    st.image('output/nuvem_palavras.png')


pagina = st.sidebar.selectbox('Página', ['Upload Json','Picos de Comentarios', 'Maiores comentaristas', 'Nuvem de Palavras'])

if pagina == 'Picos de Comentarios':
    comments_peak()
if pagina == 'Maiores comentaristas':
    most_comments()
if pagina == 'Nuvem de Palavras':
    dashboard()
else:
    landing_page()