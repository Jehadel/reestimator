# FILES TO ADD ALL FONCTIONS TO TRANSFORM FEATURES/COLUMNS
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

class Encoder():

    """ Initialize dataframe
    """
    def __init__(self, df):

        self.df = df

    def execute(self, col_name):

        L = list(self.df[col_name].unique())
        if '' in L:
            self.df[col_name].replace("", "NoValue", inplace=True) #Replace NaN by "NoCodeNature"

        ohe = OneHotEncoder(sparse = False) # Instanciate encoder
        ohe.fit(self.df[[col_name]]) # Fit encoder  ---> OneHotEncoder(sparse=False)

        col_encoded = ohe.transform(self.df[[col_name]]) # Encode

        dicts_col = {}
        keys = list(ohe.categories_[0])
        values = col_encoded.T.astype(int)

        for i,j in enumerate(keys):
            dicts_col[j] = values[i,:]

        result = pd.DataFrame.from_dict(dicts_col)

        self.df = self.df.reset_index(drop=True)

        #Concat df and result dataframes
        data_res = pd.concat([self.df, result], axis = 1)

        if 'NoValue' in list(data_res.columns):
            data_res = data_res.drop(columns= ['NoValue',col_name] )
        else:
            data_res = data_res.drop(columns= col_name)

        return data_res
