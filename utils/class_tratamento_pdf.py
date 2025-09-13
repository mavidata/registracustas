import pandas as pd
import pdfplumber
import re
from pandas import DataFrame
class ExtratorHotelBrasilHistoria:
    def __init__(self):
        pass

    def __extrair_linhas(self, caminho_pdf: str):
        linhas = []
        with pdfplumber.open(caminho_pdf) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text()
                if texto:
                    linhas.extend(texto.split("\n"))
        return linhas

    def __montar_registros(self, linhas: list):
        registros = []
        buffer = None

        for linha in linhas:
            l = linha.strip()

            if re.search(r"\d{2}/\d{2}/\d{4}$", l):
                partes = l.split()
                data = partes[-1]
                preco = partes[-2]

                qnt_idx = None
                for i, p in enumerate(partes):
                    if p.isdigit():
                        qnt_idx = i
                        break

                if qnt_idx is None:
                    continue  

                qnt = partes[qnt_idx]
                comprador = " ".join(partes[qnt_idx+1:-2])
                produto = buffer if buffer else " ".join(partes[:qnt_idx])

                registros.append({
                    "Produto": produto.strip(),
                    "Quantidade": int(qnt),
                    "Comprador": comprador.strip(),
                    "Preço Unitário": float(preco.replace(".", "").replace(",", ".")),
                    "Data Referência": pd.to_datetime(data, dayfirst=True)
                })
                buffer = None
            else:
                buffer = f"{buffer} {l}" if buffer else l


        return registros
    
    def _renomeia_colunas(self, registros: DataFrame) -> DataFrame:

        registros = DataFrame(registros)

        registros.rename(
            columns={
                "Comprador": "Nome Colaborador",
                "Produto": "Item Consumido",
                "Quantidade": "Quantidade Itens",
                "Data Referência": "Data Consumo",
                "Preço Unitário": "Valor",
            },
            inplace=True
        )

        return registros

    def __tipo_colunas(self, registros: DataFrame) -> DataFrame:

        registros["Data Consumo"] = pd.to_datetime(
            registros["Data Consumo"], errors="coerce", dayfirst=True
        ).dt.strftime("%d/%m/%Y")

        return registros
    


    def executar(self, caminho_pdf: str) -> DataFrame:
        linhas = self.__extrair_linhas(caminho_pdf)
        registros = self.__montar_registros(linhas)
        registros_renomeados = self._renomeia_colunas(registros)
        registros_formatos = self.__tipo_colunas(registros_renomeados)
        return registros_formatos


    

