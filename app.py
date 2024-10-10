import streamlit as st
from member_count import get_new_members
from nuvem import gerar_nuvem_palavras, file_to_json
from stats import get_top_authors, get_author_comments
from particoes import get_partitions
from peaks import get_peaks, get_top_words, get_word_context
import plotly.graph_objects as go

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

            st.write(get_word_context(peak['messages'], word))

                        


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
            top_words_count = get_top_words(partition['comments'])
            top_words = top_words_count.index.to_list()
            word = st.selectbox('Top words', top_words)

            st.write(get_word_context(partition['comments'], word))

def show_stats():
    st.title('Key Stats')

    comments_data = file_to_json(st.session_state['comments_json'])

    total_comments = len(comments_data)
    total_authors = len(set([comment["author"] for comment in comments_data]))
    avg_comments_per_person = total_comments / total_authors
    total_words = sum([len(comment["message"].split()) for comment in comments_data])
    unique_words = len(set([word for comment in comments_data for word in comment["message"].split()]))
    avg_words_per_comment = total_words / total_comments
    _, new_mem = get_new_members(comments_data)
    new_members_count = len(new_mem)

    def create_card(title, value, card_color="lightgray", text_color="black"):
        fig = go.Figure(go.Indicator(
            mode="number",
            value=value,
            title={"text": title, "font": {"size": 24, "color": text_color}},
            number={"font": {"size": 40, "color": text_color}},
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        
        fig.update_layout(
            paper_bgcolor=card_color,
            margin=dict(l=20, r=20, t=50, b=50),
            height=200
        )
        return fig

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.plotly_chart(create_card("Total Comments", total_comments, card_color="lightblue", text_color="darkblue"), use_container_width=True)
        st.plotly_chart(create_card("Total Words", total_words, card_color="lightgreen", text_color="darkgreen"), use_container_width=True)

    with col2:
        st.plotly_chart(create_card("Total Authors", total_authors, card_color="lightyellow", text_color="darkorange"), use_container_width=True)
        st.plotly_chart(create_card("Unique Words", unique_words, card_color="lightpink", text_color="darkred"), use_container_width=True)

    with col3:
        st.plotly_chart(create_card("Avg Comments/Person", avg_comments_per_person, card_color="lightgray", text_color="black"), use_container_width=True)
        st.plotly_chart(create_card("New Members", new_members_count, card_color="lightgray", text_color="black"), use_container_width=True)

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
