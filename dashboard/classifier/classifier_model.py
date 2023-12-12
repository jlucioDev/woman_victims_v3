import pandas as pd
import numpy as np
from pyDecision.algorithm import electre_tri_b
import pickle
from electre_tree import tree_e_tri_b , util_e_tri_b



from sklearn.model_selection import train_test_split

class classifierModel:
    
    def __init__(self, state: str) -> None:
        self.state = state # Estado da federação
        self.B = [] # Limites
        self.W = [] # Pesos
        self.P = [] # Preferência forte
        self.Q = [] # Preferência fraca
        self.V = [] # veto
        self.fig_predict = []
        self.fig_classify = []

        

    def create_classification(self, df: pd.DataFrame, criteria_list: list, classify_type: str):
        df_classification = df[criteria_list]

        if classify_type == 'QuantClass':            
            cc = self.quartile_classifier(df_classification)
            return cc
        elif classify_type == 'RandFloClass':
            cc = self.random_forest_classifier(df_classification)
            return cc
        else:
            pass # retorna uma exceção
        

    
    def quartile_classifier(self, df_criteria: pd.DataFrame):
        columns_count = len(df_criteria.columns)
        b = []
        b.append(df_criteria.quantile(0.25))
        b.append(df_criteria.quantile(0.75))
        b.append(df_criteria.quantile(0.90))
      
          
        self.B = np.array(b).tolist()
        
        self.Q = [0.0]*columns_count
        self.P = [0.0]*columns_count
        self.V = [0.0]*columns_count
        self.W = [0.0]*columns_count
        if "IAP" in df_criteria.columns:
            indice_coluna = df_criteria.columns.get_loc("IAP")
            self.W[indice_coluna] = 0.6

        

        print(f''' 
        Número de colunas: {columns_count} \n
        B = {self.B}
        Q = {self.Q}
        P = {self.P}
        V = {self.V}
        W = {self.W}
        ''')

        print(df_criteria)
        # Retorna a classificação
        return electre_tri_b(
            np.array(df_criteria), 
            self.W , 
            self.Q , 
            self.P , 
            self.V , 
            self.B , 
            cut_level = 0.65, 
            verbose = False, 
            rule = 'pc', 
            graph = False)

    def random_forest_classifier(self, df_criteria):
        columns_count = len(df_criteria.columns)
        
        X = df_criteria.values
        #print(df_criteria)

        # Parameters - ELECTRE Tree
        rule      = 'pc'
        classes   = 4
        target    = []
    
        # Iniciação dos parâmetros
        cut_level = [0.5, 1.0]
        self.Q         = [] #[0.15, 0.12, 0.11, 0.12]
        self.P         = [] #[0.22, 0.14, 0.17, 0.24]
        self.V         = [] #[0.44, 0.27, 0.22, 0.35]
        self.W = [0.0]*columns_count
        if "IAP" in df_criteria.columns:
            indice_coluna = df_criteria.columns.get_loc("IAP")
            self.W[indice_coluna] = 0.6
        print(self.W)

        #self.W = [0.6,     0.0,      0.0,     0.0]
        self.B         = []
        models    = 10 # 200

        # Parameters - GA
        elite       = 2 #     1 
        eta         = 1 #     1
        mu          = 1 #     1
        size        = 15 #    15
        rate        = 0.2 #  0.05
        generations = 30 #    30
        samples     = 0.10 #  10

        models = tree_e_tri_b.tree_electre_tri_b(
            X,
            target_assignment = target, 
            W = self.W, 
            Q = self.Q, 
            P = self.P, 
            V = self.V, 
            B = self.B, 
            cut_level = cut_level, 
            rule = rule, 
            number_of_classes = classes, 
            elite = elite, 
            eta = eta, 
            mu = mu, 
            population_size = size, 
            mutation_rate = rate, 
            generations = generations, 
            samples = samples, 
            number_of_models = models)   
        # with open('datasets/models_treinado_acc_84.pkl', 'rb') as f:
        #     models_saved = pickle.load(f)
        # models = models_saved

        # Predict
        prediction, solutions = tree_e_tri_b.predict(models, X, verbose = False, rule = rule)

        # Plot - Tree Model
        #self.fig_classify =  util_e_tri_b.plot_points(X, prediction)
        util_e_tri_b.plot_points(X, prediction)

        w_mean, w_std, q_mean, q_std, p_mean, p_std, v_mean, v_std, b_mean, b_std, cut_mean, cut_std, acc_mean, acc_std = tree_e_tri_b.metrics(models, number_of_classes = classes)
        print(f'''
            Média Acurácia: {acc_mean}
            Desvio Acurácia: {acc_std}

        ''')
        return util_e_tri_b.electre_tri_b(
            X, 
            W = w_mean, 
            Q = q_mean, 
            P = p_mean, 
            V = v_mean, 
            B = b_mean, 
            cut_level = cut_mean, 
            verbose = False, 
            rule = rule, 
            graph = False)
    

