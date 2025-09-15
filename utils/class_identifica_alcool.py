from pandas import DataFrame
import numpy as np

class IdentificaAlcool:
    def __init__(self):
        pass

    def valida_alcool(self, dataframe: DataFrame) -> DataFrame:
 
        bebidas_alcoolicas = [
            "cerveja",
            "vinho",
            "champanhe",
            "espumante",
            "vodka",
            "uísque",
            "whisky",  
            "cachaça",
            "rum",
            "gin",
            "tequila",
            "conhaque",
            "licor",
            "absinto",
            "saké",
            "mead",     
            "cidra",
            "vermouth",
            "grappa",
            "pisco",
            "bourbon",
            "brandy",
            "porto",
            "xerez",    
            "campari",
            "amaro",
            "aperol",
            "baileys",
            "martini",
            "margarita"
        ]
        dataframe["Flag Alcoólico"] = np.where(dataframe["Item Consumido"].str.lower().str.contains("|".join(bebidas_alcoolicas)) , "True", "False")

        return dataframe

