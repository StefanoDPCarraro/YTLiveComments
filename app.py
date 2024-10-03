import streamlit as st
from member_count import get_new_members
from nuvem import gerar_nuvem_palavras, file_to_json
from stats import get_top_authors, get_author_comments
from particoes import get_partitions
from peaks import get_peaks, get_top_words, get_word_context

st.session_state['comments_json'] = 'comments.json'
st.session_state['partitions'] = get_partitions(st.session_state['comments_json'])

def landing_page():
    st.title('In progress')

    st.write('Select one of the options on the sidebar to start analyzing the comments')

def comments_peak():
    st.title('Comments Peak')
    num_peaks = st.slider('Number of peaks on display', 1, 15, 5)
    peaks, image_path = get_peaks(st.session_state['comments_json'], top=num_peaks)
    st.image(image_path)
    for index, peak in enumerate(peaks):
        with st.expander(f'Peak {index+1}: {peak["comments"]} comments'):
            st.write(f'Start: {peak["start"]}')
            st.write(f'End: {peak["end"]}')
            st.image(gerar_nuvem_palavras(peak['messages'], complemento=f'_pico_{index}'))
            top_words_count = get_top_words(peak['messages'], n = 50)
            top_words = top_words_count.index.to_list()
            word = st.selectbox('Top words', top_words)
            print("Selected word:", word)

            st.write(get_word_context(peak['messages'], word))
            print(top_words)

                        


def most_comments():
    st.title('Top commenters')
    n_authors = st.slider('Number of commenters on display', 1, 10, 5)
    if st.session_state['comments_json'] is not None:
        authors = get_top_authors(st.session_state['comments_json'], n=n_authors)
        for author, count in authors:
            with st.expander(f'{author}: {count} comments'):
                path, comments = get_author_comments(author, 'comments.json')
                st.image(path)
                for comment in comments:
                    st.write(f"{comment['time_elapsed']} - {comment['message']}")

def show_partitions():
    st.title('Partitions')
    num_part = st.slider('Number of partitions on display', 1, 10, 5)
    st.session_state['partitions'] = get_partitions(st.session_state['comments_json'], n=num_part)
    for index, partition in st.session_state['partitions'].items():
        with st.expander(f'Partition {index+1}'):
            st.write(f'Comments: {len(partition["comments"])}')
            st.write(f'Start: {partition["start"]}')
            st.write(f'End: {partition["end"]}')
            st.image(gerar_nuvem_palavras(partition['comments'], complemento=f'_particao_{index}'))

def show_stats():
    st.title('Stats')
    comments_data = file_to_json(st.session_state['comments_json'])
    st.write(f'Total comments: {len(comments_data)}')
    st.write(f'Total comment authors: {len(set([comment["author"] for comment in comments_data]))}')
    st.write(f'Average of comments by person: {len(comments_data) / len(set([comment["author"] for comment in comments_data]))}')
    st.write(f'Total words: {sum([len(comment["message"].split()) for comment in comments_data])}')
    st.write(f'Total unique words: {len(set([word for comment in comments_data for word in comment["message"].split()]))}')
    st.write(f'Average words by comment: {sum([len(comment["message"].split()) for comment in comments_data]) / len(comments_data)}')
    _, new_mem = get_new_members(comments_data)
    st.write(f'New members count: {len(new_mem)}')

def show_new_members():
    st.title('Membros')
    member_data = file_to_json(st.session_state['comments_json'])
    path, members = get_new_members(member_data)
    st.image(path)
    with st.expander('New members', expanded=True):
        for member in members:
            st.write(f'{member["author"]} - {member["time_elapsed"]}')

pagina = st.sidebar.selectbox('Page', ['Upload Json','Comments peak', 'Top comment authors', 'Partitions', 'Stats', 'New members'])

if pagina == 'Comments peak':
    comments_peak()
elif pagina == 'Top comment authors':
    most_comments()
elif pagina == 'Partitions':
    show_partitions()
elif pagina == 'Stats':
    show_stats()
elif pagina == 'New members':
    show_new_members()
else:
    landing_page()
