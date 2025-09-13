from pandas import DataFrame
import pandas as pd

class ExtratorHotelBravo:
    def __init__(self):
        pass

    def __seleciona_colunas(self, dataframe: DataFrame) -> DataFrame:
        dataframe = dataframe[
            [
                "DATA DA COMPRA",
                "ITEM",
                "QUANTIDADE REFERÊNCIA",
                "VALOR ITEM",
                "CONSUMIDOR",
            ]
        ]
        return dataframe

    def __nome_colunas(self, dataframe: DataFrame) -> DataFrame:
        dataframe.rename(
            columns={
                "DATA DA COMPRA": "Data Consumo",
                "ITEM": "Item Consumido",
                "QUANTIDADE REFERÊNCIA": "Quantidade Itens",
                "VALOR ITEM": "Valor",
                "CONSUMIDOR": "Nome Colaborador",
            },
            inplace=True,
        )

        dataframe["Data Consumo"] = pd.to_datetime(
            dataframe["Data Consumo"], errors="coerce", dayfirst=True
        ).dt.strftime("%d/%m/%Y")

        return dataframe

    def executar(self, dataframe: DataFrame) -> DataFrame:
        dataframe = self.__seleciona_colunas(dataframe)
        dataframe = self.__nome_colunas(dataframe)
        return dataframe


