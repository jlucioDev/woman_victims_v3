import requests
import pandas as pd
import numpy as np
import os
# AHP
from pyDecision.algorithm import ahp_method

#Buscador de dados do IBGE
class IBGEDataFetcher:

    # Lista de abreviações válidas dos estados brasileiros
    ESTADOS_BRASILEIROS = [
        'ac', 'al', 'am', 'ap', 'ba', 'ce', 'df', 'es', 'go', 'ma', 'mg', 'ms',
        'mt', 'pa', 'pb', 'pe', 'pi', 'pr', 'rj', 'rn', 'ro', 'rr', 'rs', 'sc',
        'se', 'sp', 'to'
    ]
    
    BASE_URL = "http://servicodados.ibge.gov.br/api/v1/localidades/estados"
    
        
    def __init__(self, state: str):
        # Verifica se a abreviação do estado é válida
        if state.lower() not in self.ESTADOS_BRASILEIROS:
            raise ValueError("A abreviação do estado não é válida.")
        self.state = state.lower()

    def fetch_municipalites_info(self) -> pd.DataFrame:
        # Verifica se existe um dataset (arquivo)
        if not os.path.exists(f"datasets/indicators_{self.state.lower()}.parquet"):
            # Prepara o sufixo da url
            endpoint = f'/{self.state}/municipios'

            # Busca os dados (id e nome) dos municípios
            data = self.fetch_api_data(endpoint)

            # Formata os ids
            data = self.format_ids(data)

            # transforma em dataframe
            df = self.transform_to_dataframe(data)

            # cria um lista com os ids dos municípios.
            lst_municipalites = self.municipalites_to_list(df)

            # Adiciona os dados dos critérios usando as subclasses
            idh_data = IDHDataFetcher(self.state, lst_municipalites)
            pib_data = PIBDataFetcher(self.state, lst_municipalites)
            gini_data = GINIDataFetcher(self.state, lst_municipalites)
            iap_data = IAPDataFetcher(self.state, lst_municipalites)

            df = iap_data.add_data(df, "IAP")
            df = idh_data.add_data(df, "IDH")
            df = pib_data.add_data(df, "PIB")
            df = gini_data.add_data(df, "GINI")

            # Salva os dataframe principal com os dados dos indicadores em um arquivo.
            df.to_parquet(f"datasets/indicators_{self.state.lower()}.parquet")
        else:
            # Ler arquivo salvo
            df = pd.read_parquet(f"datasets/indicators_{self.state.lower()}.parquet")

        return df


    def fetch_api_data(self, endpoint: str) -> dict:
        url = f'{self.BASE_URL}/{endpoint}'
        response = requests.get(url)
        data = response.json()
        return data

    def transform_to_dataframe(self, data: dict) -> pd.DataFrame:
        # Implemente a lógica para transformar os dados em um DataFrame Pandas
        df = pd.DataFrame(data, columns=["id", "nome"])
        df.rename(columns={'nome': 'localidade'}, inplace=True)
        return df

    def municipalites_to_list(self, df: pd.DataFrame):
        # Extrai os IDs do DataFrame e converte-os em uma lista
        ids = df['id'].tolist()
        # Converte a lista de IDs em uma string separada por "|"
        ids_str = '|'.join(map(str, ids))
        #returna a string com os IDs dos municípios
        return ids_str

    def format_ids(self, idata: str):
        # Remove o último dígito da chave "id" em cada dicionário
        # Isso corrige as futuras buscar por ids.
        for item in idata:
            if 'id' in item:
                item['id'] = int(str(item['id'])[:-1])
            
        return idata
    
class IBaseFetcher:
    BASE_URL = "https://servicodados.ibge.gov.br/api/v1/pesquisas"
    

    def __init__(self, state: str, municipalites: str):
        self.state = state
        self.municipalites = municipalites

    def fetch_api_data(self, endpoint: str) -> dict:
        url = f'{self.BASE_URL}/{endpoint}'
        response = requests.get(url)
        data = response.json()[0]["res"]
        return data

    def fetch_api_dataframe(self) -> pd.DataFrame:
        # Implemente a lógica para buscar o indicador específico
        # Retorne um DataFrame com os dados do indicador
        pass

    def add_data(self, df, indicator_name: str) -> pd.DataFrame:
        
        # busca os dados 
        df_indicador_data = self.fetch_api_dataframe()

        # Converte as colunas id dos dois dataframes para int
        # Isso foi necessário para corrigir o merge entre eles.
        df['id'] = df['id'].astype(int)
        df_indicador_data['id'] = df_indicador_data['id'].astype(int)
       
        df = pd.merge(df, df_indicador_data, on='id', how='outer')

        # Substituir valores NaN por 0 em todas as colunas
        df.fillna(0, inplace=True)

        return df
    

class IDHDataFetcher(IBaseFetcher):
    NUM = "37"
    YEAR = "2010"
    INDICATOR = "30255"

    def fetch_api_dataframe(self) -> pd.DataFrame:
        # Implemente a lógica para buscar o indicador IDH
        endpoint = f"{self.NUM}/periodos/{self.YEAR}/indicadores/{self.INDICATOR}/resultados/{self.municipalites}"
        data = self.fetch_api_data(endpoint)
        # Transforma os dados em uma lista aninhada
        nested_data = [{'id': item['localidade'], 'IDH': item['res'][self.YEAR]} for item in data]

        # Usa a função json_normalize
        df = pd.json_normalize(nested_data)

        #Converte os dados para valores numéricos
        df['IDH'] = pd.to_numeric(df['IDH'], errors='coerce')

        # Substituir valores diferentes de floar para 0.0
        df['IDH'] = df['IDH'].apply(lambda x: float(x) if isinstance(x, float) else 0.0)

        return df

class PIBDataFetcher(IBaseFetcher):
    NUM = "38"
    YEAR = "2019"
    INDICATOR = "47001"

    def fetch_api_dataframe(self) -> pd.DataFrame:
        # Implemente a lógica para buscar o indicador IDH
        endpoint = f"{self.NUM}/periodos/{self.YEAR}/indicadores/{self.INDICATOR}/resultados/{self.municipalites}"
        data = self.fetch_api_data(endpoint)
        # Transforma os dados em uma lista aninhada
        nested_data = [{'id': item['localidade'], 'PIB': item['res'][self.YEAR]} for item in data]

        # Usa a função json_normalize
        df = pd.json_normalize(nested_data)

        #Converte os dados para valores numéricos
        df['PIB'] = pd.to_numeric(df['PIB'], errors='coerce')
        
        # Substituir valores diferentes de floar para 0.0
        df['PIB'] = df['PIB'].apply(lambda x: float(x) if isinstance(x, float) else 0.0)

        return df

class GINIDataFetcher(IBaseFetcher):
    NUM = "36"
    YEAR = "2003"
    INDICATOR = "30252"

    def fetch_api_dataframe(self) -> pd.DataFrame:
        # Implemente a lógica para buscar o indicador IDH
        endpoint = f"{self.NUM}/periodos/{self.YEAR}/indicadores/{self.INDICATOR}/resultados/{self.municipalites}"
        data = self.fetch_api_data(endpoint)

        # Transforma os dados em uma lista aninhada
        nested_data = [{'id': item['localidade'], 'GINI': item['res'][self.YEAR]} for item in data]

        # Usa a função json_normalize
        df = pd.json_normalize(nested_data)
        
        #Converte os dados para valores numéricos
        df['GINI'] = pd.to_numeric(df['GINI'], errors='coerce')

        # Transforma os valores para o complementar.
        df['GINI'] = 1 - df['GINI']

        # Substituir valores diferentes de floar para 0.0
        df['GINI'] = df['GINI'].apply(lambda x: float(x) if isinstance(x, float) else 0.0)

        return df

class IAPDataFetcher(IBaseFetcher):
    NUM = "1"
    YEAR = "2019"
    INDICATOR = ['90201','90335','90358','90626','90640', '90272', '90397']
    
    # g1 - 90201: Delegacia especializada no Atendimento à Mulher
    # g2 - 90358: Ações de Enfrentamento à Violência contra a Mulher
    # g3 - 90626: Direitos ou política para mulheres
    # g4 - 90335: Executa programas e ações para grupos específicos - Mulheres
    # g5 - 90640: Políticas ou programas na área de direitos humanos - Proteção de mulheres vítimas de violência doméstica 
    # g6 - 90272: Ações Socioeducativas - Violência doméstica e de gênero
    # g7 - 90397: Constituição de centros de referência e atendimento em direitos humanos
        
    def fetch_api_data(self, endpoint: str) -> dict:
        url = f'{self.BASE_URL}/{endpoint}'
        response = requests.get(url)
        data = response.json()
        return data

    def fetch_api_dataframe(self) -> pd.DataFrame:
        # O Índice será calculado conforme os indicadores de 
        # assistencias e proteção à mulher vítima de violência.

        # Implemente a lógica para buscar o indicador IDH
        endpoint = f"{self.NUM}/periodos/{self.YEAR}/indicadores/{'|'.join(map(str, self.INDICATOR))}/resultados/{self.municipalites}"
        data = self.fetch_api_data(endpoint)

        #Calcula os pesos dos indicadores
        weightAHP = self.weight_by_ahp()

        #Calcula o IAP
        df = self.iap_calculator(data, weightAHP)
        
        return df

    def weight_by_ahp(self):

        # link online
        # https://bpmsg.com/ahp/ahp-calc.php?n=7&t=AHP+priorities&c[0]=Delegacia+especializada&c[1]=A%C3%A7%C3%B5es+de+Enfrentamento&c[2]=A%C3%A7%C3%B5es+Socioeducativas&c[3]=Pol%C3%ADticas+DH&c[4]=Direitos+ou+pol%C3%ADtica+para+mulheres&c[5]=Executa+programas+e+a%C3%A7%C3%B5es&c[6]=centros+de+refer%C3%AAncia
        # Parameters
        weight_derivation = 'geometric' # 'mean'; 'geometric' or 'max_eigen'

        # Dataset
        dataset = np.array([
        #g1     g2     g3     g4     g5     g6     g7
        [1  ,   1  ,   5  ,   4  ,   1  ,   2  ,   5  ],   #g1
        [1  ,   1  ,   2  ,   1  ,   2  ,   2  ,   5  ],   #g2
        [1/5,   1/2,   1  ,   1/4,   1/4,   1/5,   2  ],   #g3
        [1/4,   1  ,   4  ,   1  ,   1/2,   1/2,   5  ],   #g4
        [1  ,   1/2,   4  ,   2  ,   1  ,   2  ,   5  ],   #g5
        [1/2,   1/2,   5  ,   2  ,   1/2,   1  ,   5  ],   #g6
        [1/5,   1/5,   1/2,  1/5 ,   1/5,   1/5,   1  ]    #g7
        ])
    
        # Call AHP Function
        weights, rc = ahp_method(dataset, wd = weight_derivation)

        wIAP = [round(valor, 2) for valor in weights.tolist()]
        wIAP = sorted(wIAP, reverse=True)

        selected_indicators = [90201, 90358, 90626, 90335, 90640, 90272, 90397]
   

        # Crie um dicionário a partir das duas listas
        weightDic = {}
        for i in range(len(selected_indicators)):
            weightDic[selected_indicators[i]] = wIAP[i]
        
        return weightDic

    def iap_calculator(self, data, wdic: dict):

        #dd  = [item["localidade"] for item in data]

        df = pd.DataFrame(data[0]["res"])
        df = df[['localidade']]
        df.rename(columns={'localidade': 'id'}, inplace=True)

        for indicador in data:

                valores = []
                for resultado in indicador['res']:
                        localidade = resultado['localidade']
                        valor = resultado['res']['2019']
                        if valor.lower() == 'sim':
                                valores.append({'id': localidade , indicador['id']: wdic[indicador['id']]})
                        else:
                                valores.append({'id': localidade , indicador['id']: 0})
                df[indicador['id']] = pd.DataFrame(valores, columns=[indicador['id']])
                
        # Adicionando uma coluna de total
        # Adiciona uma coluna chamada 'Total' com a soma das outras colunas
        df['IAP'] = df.iloc[:, 1:].sum(axis=1)
        df = df[['id', 'IAP']]
        return df


# Exemplo de uso:
# state = 'pa'  # Exemplo: Pará
# fetcher = IBGEDataFetcher(state)
# result = fetcher.fetch_municipalites_info()
# print(result)
