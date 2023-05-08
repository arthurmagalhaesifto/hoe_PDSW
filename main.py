import streamlit as st
from PIL import Image

image1 = Image.open('sementeAlface.png')
image2 = Image.open('sementeAbobrinha.png')
texto_negrito1 = "<h5 style='text-align:Center'>Sementas de Alface<h5>"
texto_negrito2 = "<h5 style='text-align:Center'>Sementes de Abobrinha<h5>"

col1, col2 = st.columns(2)

with col1:
   st.markdown(texto_negrito1, unsafe_allow_html=True)
   st.image(image1, use_column_width=True)
   if st.button("OMPRAR Sementas de Alface"):
       st.write("Você clicou no botão!")

with col2:
   st.markdown(texto_negrito2, unsafe_allow_html=True)
   st.image(image2)
   if st.button("COMPRAR Sementas de Abobrinha"):
       st.write("Você clicou no botão!")