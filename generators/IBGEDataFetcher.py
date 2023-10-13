import requests
import pandas as pd

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

        #df = indicador_iap.add_indicador(df, "IAP")
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

    #90201: Delegacia especializada no Atendimento à Mulher
    #90358: Ações de Enfrentamento à Violência contra a Mulher
    #90272: Ações Socioeducativas - Violência doméstica e de gênero
    
    #90640: Políticas ou programas na área de direitos humanos - Proteção de mulheres vítimas de violência doméstica 
    #90626: Direitos ou política para mulheres
    
    #90335: Executa programas e ações para grupos específicos - Mulheres
    #90397: Constituição de centros de referência e atendimento em direitos humanos
        

    def find_indicator(self) -> pd.DataFrame:
        # Implemente a lógica para buscar o indicador IAP
        pass



# Exemplo de uso:
state = 'pa'  # Exemplo: Pará
fetcher = IBGEDataFetcher(state)
result = fetcher.fetch_municipios_info()
print(result)
