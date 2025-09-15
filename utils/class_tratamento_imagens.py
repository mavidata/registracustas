import pandas as pd
import easyocr
import re
from PIL import Image
import numpy as np
from pandas import DataFrame

class ExtratorHotelHold:
    def __init__(self):
        self.leitor = easyocr.Reader(["pt"])

    def __extrair_texto(self, imagem_ou_lista):
        if hasattr(imagem_ou_lista, "read") or isinstance(imagem_ou_lista, str):
            img = Image.open(imagem_ou_lista).convert("RGB")
            arr = np.array(img)
            return self.leitor.readtext(arr, detail=0)
        return imagem_ou_lista

    def __extrair_dataframe(self, imagem_ou_lista):
        textos = self.__extrair_texto(imagem_ou_lista)

        try:
            idx_inicio = textos.index("Item") + 1
        except ValueError:
            idx_inicio = 9  

        dados = textos[idx_inicio:]

        registros = []
        i = 0
        while i < len(dados):
            data = dados[i]
            cliente = dados[i + 1]
            valor = dados[i + 2]
            valor = valor.upper().replace("RS", "").replace("R$", "").replace("S", "")
            valor = valor.replace("O", "0").replace(" ", "")
            valor = re.sub(r"[^0-9,\.]", "", valor)
            
            possivel_qtd = dados[i + 3]
            if re.match(r"^\d+$", possivel_qtd): 
                qtd = int(possivel_qtd)
                item = dados[i + 4] if i + 4 < len(dados) else ""
                i += 5
            else:
                qtd = 1
                item = possivel_qtd
                i += 4

            registros.append([data, cliente, valor, qtd, item])

        df = pd.DataFrame(registros, columns=[
            "Data Consumo", "Nome Colaborador", "Valor", "Quantidade Itens", "Item Consumido"
        ])

        df["Valor"] = (
            df["Valor"]
            .str.replace("R\$", "", regex=True)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

        return df

    def executar(self, imagem_ou_lista):
        return self.__extrair_dataframe(imagem_ou_lista)