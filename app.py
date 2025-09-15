import streamlit as st
import pandas as pd 
from utils.class_tratamento_excel import ExtratorHotelBravo
from utils.class_tratamento_imagens import ExtratorHotelHold
from utils.class_tratamento_pdf import ExtratorHotelBrasilHistoria
from utils.class_google_sheets import HotelMakerGoogleSheets
from utils.class_identifica_alcool import IdentificaAlcool

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

st.session_state.valido = False

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
                df_processado["Nome Hotel"] = "Hotel Bravo"


            elif extensao == "png":
                extrator = ExtratorHotelHold()
                df_processado = extrator.executar(arquivo)
                df_processado["Nome Hotel"] = "Hotel Hold"

            elif extensao == "pdf":
                extrator = ExtratorHotelBrasilHistoria()
                df_processado = extrator.executar(arquivo)
                df_processado["Nome Hotel"] = "Hotel Brasil História"

            lista_dfs.append(df_processado)

            st.session_state.valido = True
            loading_run.empty()

        except Exception as err:
            loading_run.empty()
            st.error(f"Ocorreu um erro com {arquivo.name}: {err}")

    if lista_dfs:
        custos_compilados = pd.concat(lista_dfs, ignore_index=True)
        identificador = IdentificaAlcool()
        df_processado = identificador.valida_alcool(custos_compilados)
        df_processado.sort_values(by="Data Consumo")
        st.success("Processamento concluído!")
        st.dataframe(df_processado)
        
    if st.session_state.valido and st.button("Enviar ao Sheets"):

        try:
            loading_run.image(loading, width=90)

            sheets = HotelMakerGoogleSheets()
            sheets.append("Gastos Colaboradores", df_processado)
            st.success("Enviado para a Fonte de Dados!")
            loading_run.empty()
        except Exception as e:
            st.error(f"Erro ao enviar para fonte de dados")
            loading_run.empty()


