import pandas as pd
import easyocr
import re
from PIL import Image
import numpy as np

class ExtratorHotelHold:
    def __init__(self):
        self.leitor = easyocr.Reader(["pt"])
    
    def __extrair_texto(self, imagem_custos):
        if hasattr(imagem_custos, "read"):
            img = Image.open(imagem_custos).convert("RGB")
            arr = np.array(img)
            return self.leitor.readtext(arr, detail=0)

        return self.leitor.readtext(imagem_custos, detail=0)
    
    def __extrair_dataframe(self, imagem_custos):
        textos = self.__extrair_texto(imagem_custos)
        registros = []

        for i, token in enumerate(textos):
            if re.match(r"\d{2}/\d{2}/\d{4}", token):  
                try:
                    data = token
                    cliente = textos[i+1]
                    valor = textos[i+2].replace("RS", "R$").replace("O", "0")
                    qtd = int(textos[i+3]) if textos[i+3].isdigit() else 1
                    item = textos[i+4]
                    registros.append([data, cliente, valor, qtd, item])
                except IndexError:
                    pass

        custos = pd.DataFrame(registros, columns=["Data", "Cliente", "Valor", "Qtd", "Item"])

        custos["Valor"] = (
                custos["Valor"]
                .str.replace("R$", "", regex=False)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
                .astype(float)
            )

        return custos

    def __renomear_dataframe(self, custos):

        custos.rename(columns={"Data": "Data Consumo",
                                "Cliente": "Nome Colaborador",
                                "Valor": "Valor",
                                "Qtd": "Quantidade Itens",
                                "Item": "Item Consumido"},
                                    inplace=True
)
        
        return custos
    
    def executar(self, imagem_custos):
        resultado = self.__extrair_dataframe(imagem_custos)
        resultado_renomeado = self.__renomear_dataframe(resultado)
        return resultado_renomeado



    

