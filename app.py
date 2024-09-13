import streamlit as st
from member_count import get_new_members
from nuvem import gerar_nuvem_palavras, file_to_json
from stats import get_top_authors, get_author_comments
from particoes import get_partitions
from peaks import get_peaks

st.session_state['comments_json'] = 'comments.json'
st.session_state['partitions'] = get_partitions(st.session_state['comments_json'])

def landing_page():
    st.title('Análise de chat')

    if st.button('Iniciar análise'):
        analyze_chat(st.session_state['comments_json'])

def analyze_chat(comments_json):
    if comments_json is not None:
        comments_data = file_to_json(comments_json)
        gerar_nuvem_palavras(comments_data)
    else:
        st.error('Faça o upload do arquivo de comentários')

def comments_peak():
    st.title('Picos de Comentários')
    num_peaks = st.slider('Número de picos', 1, 10, 5)
    peaks, image_path = get_peaks(st.session_state['comments_json'], top=num_peaks)
    st.image(image_path)
    for index, peak in enumerate(peaks):
        with st.expander(f'Pico {index+1}: {peak["comments"]} comentários'):
            st.write(f'Início: {peak["start"]}')
            st.write(f'Fim: {peak["end"]}')
            st.image(gerar_nuvem_palavras(peak['messages'], complemento=f'_pico_{index}'))


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

def show_partitions():
    st.title('Partições')
    num_part = st.slider('Número de partições', 1, 10, 5)
    st.session_state['partitions'] = get_partitions(st.session_state['comments_json'], n=num_part)
    for index, partition in st.session_state['partitions'].items():
        with st.expander(f'Partição {index+1}'):
            st.write(f'Comentários: {len(partition["comments"])}')
            st.write(f'Início: {partition["start"]}')
            st.write(f'Fim: {partition["end"]}')
            st.image(gerar_nuvem_palavras(partition['comments'], complemento=f'_particao_{index}'))

pagina = st.sidebar.selectbox('Página', ['Upload Json','Picos de Comentarios', 'Maiores comentaristas', 'Particoes', 'Estátisticas', 'Membros'])

if pagina == 'Picos de Comentarios':
    comments_peak()
elif pagina == 'Maiores comentaristas':
    most_comments()
elif pagina == 'Particoes':
    show_partitions()
elif pagina == 'Estátisticas':
    st.title('Estatísticas')
    comments_data = file_to_json(st.session_state['comments_json'])
    st.write(f'Número total de comentários: {len(comments_data)}')
    st.write(f'Número total de pessoas que comentaram: {len(set([comment["author"] for comment in comments_data]))}')
    st.write(f'Média de comentários por pessoas: {len(comments_data) / len(set([comment["author"] for comment in comments_data]))}')
    st.write(f'Número total de palavras: {sum([len(comment["message"].split()) for comment in comments_data])}')
    st.write(f'Número total de palavras únicas: {len(set([word for comment in comments_data for word in comment["message"].split()]))}')
    st.write(f'Média de palavras por comentário: {sum([len(comment["message"].split()) for comment in comments_data]) / len(comments_data)}')
elif pagina == 'Membros':
    st.title('Membros')
    member_data = file_to_json(st.session_state['comments_json'])
    path, members = get_new_members(member_data)
    st.image(path)
    with st.expander('Novos membros', expanded=True):
        for member in members:
            st.write(f'{member["author"]} - {member["time_elapsed"]}')

else:
    landing_page()