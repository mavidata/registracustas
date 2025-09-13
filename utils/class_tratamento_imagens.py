import pandas as pd
import easyocr
import re

class ExtratorHotelHold:
    def __init__(self):
        self.leitor = easyocr.Reader(["pt"])
    
    def extrair_texto(self, imagem_custos):
        results = self.leitor.readtext(imagem_custos, detail=0)
        return results
    
    def extrair_dataframe(self, imagem_custos):
        textos = self.extrair_texto(imagem_custos)
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
    

