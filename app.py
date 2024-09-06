import streamlit as st
from PIL import Image

st.title('Image Classification')

input_link = st.text_input('Link do vídeo do youtube')

image = Image.open('output/nuvem_palavras.png')

st.image(image, caption='Uploaded Image', use_column_width=True)