import streamlit as st
import pandas as pd 


imagem_side_bar = "assets/images/hotelimage.png"

st.sidebar.image(imagem_side_bar, use_container_width=True)

st.title("Seja Bem Vindo")

with st.expander("Como Processar Os Registros de Despesas de Hotel?"):
    st.markdown("""
    1. Selecione os Arquivos em Qualquer Formato.
    2. Aguarde o Carregamento.
    3. Logo as Atualizações Constarão no BI.
    """)

st.file_uploader(label="Insira os Arquivos" , accept_multiple_files=True)

