import requests
import pandas as pd
import numpy as np
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

    def fetch_municipios_info(self) -> pd.DataFrame:
        endpoint = f'/{self.state}/municipios'
        data = self.fetch_api_data(endpoint)
        data = self.format_ids(data)
        df = self.transform_to_dataframe(data)
        lst_municipalites = self.municipalites_to_list(df)

        # Adicione os indicadores usando subclasses
        indicador_idh = IndicadorIDH(self.state, lst_municipalites)
        indicador_pib = IndicadorPIB(self.state, lst_municipalites)
        indicador_gini = IndicadorGINI(self.state, lst_municipalites)
        indicador_iap = IndicadorIAP(self.state, lst_municipalites)

        df = indicador_iap.add_indicador(df, "IAP")
        df = indicador_idh.add_indicador(df, "IDH")
        df = indicador_pib.add_indicador(df, "PIB")
        df = indicador_gini.add_indicador(df, "GINI")

        return df


    def fetch_api_data(self, endpoint: str) -> dict:
        url = f'{self.BASE_URL}/{endpoint}'
        response = requests.get(url)
        data = response.json()
        return data

    def transform_to_dataframe(self, data: dict) -> pd.DataFrame:
        # Implemente a lógica para transformar os dados em um DataFrame Pandas
        df = pd.DataFrame(data, columns=["id", "nome"])
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
        for item in idata:
            if 'id' in item:
                item['id'] = int(str(item['id'])[:-1])
            
        return idata
    
class IndicatorBase:
    BASE_URL = "https://servicodados.ibge.gov.br/api/v1/pesquisas"
    

    def __init__(self, state: str, municipalites: str):
        self.state = state
        self.municipalites = municipalites

    def fetch_api_data(self, endpoint: str) -> dict:
        url = f'{self.BASE_URL}/{endpoint}'
        response = requests.get(url)
        data = response.json()[0]["res"]
        return data

    def find_indicator(self) -> pd.DataFrame:
        # Implemente a lógica para buscar o indicador específico
        # Retorne um DataFrame com os dados do indicador
        pass

    def add_indicador(self, dataframe: pd.DataFrame, indicator_name: str) -> pd.DataFrame:
        indicador_data = self.find_indicator()

        dataframe = pd.concat([dataframe, indicador_data[indicator_name]], axis=1)
        return dataframe
    


class IndicadorIDH(IndicatorBase):
    NUM = "37"
    YEAR = "2010"
    INDICATOR = "30255"

    def find_indicator(self) -> pd.DataFrame:
        # Implemente a lógica para buscar o indicador IDH
        endpoint = f"{self.NUM}/periodos/{self.YEAR}/indicadores/{self.INDICATOR}/resultados/{self.municipalites}"
        data = self.fetch_api_data(endpoint)
        # Transforma os dados em uma lista aninhada
        nested_data = [{'id': item['localidade'], 'IDH': item['res'][self.YEAR]} for item in data]

        # Usa a função json_normalize
        df = pd.json_normalize(nested_data)
    
        return df

class IndicadorPIB(IndicatorBase):
    NUM = "38"
    YEAR = "2019"
    INDICATOR = "47001"

    def find_indicator(self) -> pd.DataFrame:
        # Implemente a lógica para buscar o indicador IDH
        endpoint = f"{self.NUM}/periodos/{self.YEAR}/indicadores/{self.INDICATOR}/resultados/{self.municipalites}"
        data = self.fetch_api_data(endpoint)
        # Transforma os dados em uma lista aninhada
        nested_data = [{'id': item['localidade'], 'PIB': item['res'][self.YEAR]} for item in data]

        # Usa a função json_normalize
        df = pd.json_normalize(nested_data)
    
        return df

class IndicadorGINI(IndicatorBase):
    NUM = "36"
    YEAR = "2003"
    INDICATOR = "30252"

    def find_indicator(self) -> pd.DataFrame:
        # Implemente a lógica para buscar o indicador IDH
        endpoint = f"{self.NUM}/periodos/{self.YEAR}/indicadores/{self.INDICATOR}/resultados/{self.municipalites}"
        data = self.fetch_api_data(endpoint)
        # Transforma os dados em uma lista aninhada
        nested_data = [{'id': item['localidade'], 'GINI': item['res'][self.YEAR]} for item in data]

        # Usa a função json_normalize
        df = pd.json_normalize(nested_data)
    
        return df

class IndicadorIAP(IndicatorBase):
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

    def find_indicator(self) -> pd.DataFrame:
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

        for indicador in data:

                valores = []
                for resultado in indicador['res']:
                        localidade = resultado['localidade']
                        valor = resultado['res']['2019']
                        if valor.lower() == 'sim':
                                valores.append({'localidade': localidade , indicador['id']: wdic[indicador['id']]})
                        else:
                                valores.append({'localidade': localidade , indicador['id']: 0})
                df[indicador['id']] = pd.DataFrame(valores, columns=[indicador['id']])
                
        # Adicionando uma coluna de total
        # Adiciona uma coluna chamada 'Total' com a soma das outras colunas
        df['IAP'] = df.iloc[:, 1:].sum(axis=1)
        df = df[['localidade', 'IAP']]
        return df


# Exemplo de uso:
state = 'pa'  # Exemplo: Pará
fetcher = IBGEDataFetcher(state)
result = fetcher.fetch_municipios_info()
print(result)
