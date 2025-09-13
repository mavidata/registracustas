import streamlit as st
import pandas as pd 
from utils.class_tratamento_excel import ExtratorHotelBravo
from utils.class_tratamento_imagens import ExtratorHotelHold
from utils.class_tratamento_pdf import ExtratorHotelBrasilHistoria
from utils.class_google_sheets import HotelMakerGoogleSheets

loading = "https://i.gifer.com/bfR.gif"


imagem_side_bar = "assets/images/hotelimage.png"

st.sidebar.image(imagem_side_bar, use_container_width=True)

st.title("Seja Bem Vindo")

with st.expander("Como Processar Os Registros de Despesas de Hotel?"):
    st.markdown("""
    1. Selecione os Arquivos em Qualquer Formato.
    2. Aguarde o Carregamento.
    3. Logo as Atualizações Constarão no BI.
    """)

arquivos = st.file_uploader(label="Insira os Arquivos" , accept_multiple_files=True)

loading_run = st.empty()

if arquivos:
    lista_dfs = []  

    for arquivo in arquivos:
        try:
            loading_run.image(loading, width=90)
            nome = arquivo.name
            extensao = nome.split(".")[-1].lower() 

            if extensao == "xlsx":
                df = pd.read_excel(arquivo, header=2)
                extrator = ExtratorHotelBravo()
                df_processado = extrator.executar(df)

            elif extensao == "png":
                extrator = ExtratorHotelHold()
                df_processado = extrator.executar(arquivo)

            elif extensao == "pdf":
                extrator = ExtratorHotelBrasilHistoria()
                df_processado = extrator.executar(arquivo)

            else:
                st.warning(f"Extensão não suportada: {nome}")
                continue

            lista_dfs.append(df_processado)


        except Exception as err:
            st.error(f"Ocorreu um erro com {arquivo.name}: {err}")

    loading_run.empty()

    if lista_dfs:
        custos_compilados = pd.concat(lista_dfs, ignore_index=True)
        sheets = HotelMakerGoogleSheets()
        sheets.append("Gastos Colaboradores", custos_compilados)
        st.success("Processamento concluído!")
        st.dataframe(custos_compilados)

