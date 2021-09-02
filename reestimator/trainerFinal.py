#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Import packages
from reestimator.Mysql_mgmt.get_data import Data_loading
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, RobustScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, RandomizedSearchCV, KFold
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression , Ridge , Lasso
from sklearn.metrics import mean_absolute_percentage_error as mape
from sklearn.metrics import mean_squared_error as rmse
import joblib
from google.cloud import storage

from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

import xgboost as xgb
from xgboost.sklearn import XGBRegressor
from xgboost import plot_importance

from scipy import stats

BUCKET_NAME='reestimator'


class Trainer():
    """ Initialize dataframe
    """
    def __init__(self, df, col_list, target_var,
                 scaler,model,params_cv, randomsearch_dict,
                                   nsplits = 10,
                                   scor = "neg_mean_absolute_error"):

        self.df = df
        self.col_list = col_list
        self.target_var = target_var
        self.scaler = scaler
        self.model = model
        self.params_cv = params_cv
        self.randomsearch_dict = randomsearch_dict
        self.nsplits = nsplits
        self.scor = scor

    def define_dataset(self, df, col_list, target_var):
        # define dataset
        y = self.df[self.target_var]
        X = self.df[self.col_list]

        return X,y


    def holdout(self, X, y):
        """ Instantiating train test split while creating
        X and y train and test variables
        """
        #X,y = self.define_dataset(self.df, self.col_list, self.target_var)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size = 0.3, random_state = 0)

        return X_train, X_test, y_train, y_test

    def scale(self, X_train, X_test):
        """instantiating the scaler
        scaling Xs"""

        #X_train, X_test, y_train, y_test = self.split_X_y_sets()
        self.scaler.fit(X_train)
        X_train_sc = self.scaler.transform(X_train)
        X_test_sc = self.scaler.transform(X_test)

        return X_train_sc, X_test_sc #, y_train, y_test


    def set_model(self, model):

        """defines the model as a class attribute"""
        '''returns a model'''
        if self.model=="Lasso":
            modelo = Lasso()
        elif self.model=="Ridge":
            modelo = Ridge()
        elif self.model == "RandomForest":
            modelo = RandomForestRegressor(random_state = 42)
        else:
            if self.model == "XGBoost":
                #modelo = xgb.XGBRegressor()
                modelo = xgb.XGBRegressor(booster = 'gbtree', objective ='reg:squarederror',
                                                colsample_bytree = 0.3, learning_rate = 0.35,
                                      max_depth = 10, alpha = 0.1, n_estimators = 500)


        return modelo


    def evaluate(self, model, X_train, X_test, y_train, y_test):
        """evaluates the pipeline on df_test and return the RMSE"""

        model.fit(X_train,y_train)
        y_pred = model.predict(X_test)
        R2 = r2_score(y_test, y_pred)
        MAE = round(mape(y_test, y_pred), 2)
        RMSE = round(rmse(y_test, y_pred), 2)

        res = {'Model': self.model, 'R2' : R2, 'MAPE': MAE, 'RMSE': RMSE}
        return res


    def get_feature_importances(self):
        """evaluates the pipeline on df_test and return the RMSE"""
        X,y = self.define_dataset(self.df, self.col_list, self.target_var)

        # execute search
        search = self.set_Randomized_search(self.model)

        X_train, X_test, y_train, y_test= self.holdout(X, y)
        X_train_sc, X_test_sc = self.scale(X_train, X_test)
        res = search.fit(X_train_sc, y_train)

        #model = self.set_model(self.model)


        if (self.model == "Lasso") | (self.model == "Ridge"):

            model = self.set_model(self.model)
            best = model.set_params(**res.best_params_)
            best.fit(X_train_sc,y_train)
            features = best.coef_

        else:
            #RandomForest or XGBoost
            model = self.set_model(self.model)
            best = model.set_params(**res.best_params_)
            best.fit(X_train_sc,y_train)
            features = pd.DataFrame(best.feature_importances_,
                        index = X_train.columns,
                    columns=['importance']).sort_values('importance', ascending=False)

        return features

    def set_Randomized_search(self, model):


        if (self.model == "Lasso") | (self.model == "Ridge"):

            model = self.set_model(self.model)

            # define cross validation
            cv = KFold(n_splits=self.nsplits)

            search_case = RandomizedSearchCV(model, self.params_cv,
                                        n_iter=self.randomsearch_dict['reg_iter'],
                                            scoring= self.scor, n_jobs=-1,
                                                cv=cv, random_state=1, verbose=2)

        else:
            if self.model == "RandomForest":

                random_forest = self.set_model(self.model)

                #random_forest = RandomForestRegressor(random_state = 42)

                search_case = RandomizedSearchCV(estimator = random_forest,
                                                 param_distributions = self.params_cv,
                   n_iter = self.randomsearch_dict['forest_iter'],
                                                 cv = 5, verbose=2, random_state=42, n_jobs = -1)

            else:
                print("**333*** ", model)

                xgboost_regression = self.set_model(self.model)

                search_case = RandomizedSearchCV(estimator = xgboost_regression,
                                       param_distributions = self.params_cv,
                                       n_iter = self.randomsearch_dict['xgboost_iter'],
                                                 cv = 3, verbose=2, #n_iter=1000
                                       random_state=0, n_jobs = -1)

        return search_case


    def execute(self):

        X,y = self.define_dataset(self.df, self.col_list, self.target_var)

        # execute search
        search = self.set_Randomized_search(self.model)

        X_train, X_test, y_train, y_test= self.holdout(X, y)
        X_train_sc, X_test_sc = self.scale(X_train, X_test)
        res = search.fit(X_train_sc, y_train)

         # summarize result
        # print('Best Score: %s' % res.best_score_)
        # print('Best Hyperparameters: %s' % res.best_params_)

        self.model = self.set_model(self.model)

        best = self.model.set_params(**res.best_params_)
        #print("model  ", model)

        # train and predict
        result = self.evaluate(best, X_train_sc, X_test_sc, y_train, y_test)

        return result

    # def save_model(self, model_name):
    #     """Save the model into a .joblib format"""
    #     joblib.dump(self.pipeline, f'{model_name}.joblib')
    #     print(colored(f"[{model_name}] saved locally", "green"))

    def save_model_to_gcp(self, model_name):
        """Save the model into a .joblib and upload it on Google Storage /models folder
        HINTS : use sklearn.joblib (or jbolib) libraries and google-cloud-storage"""
        local_model_name = f'{model_name}.joblib'
        # saving the trained model to disk (which does not really make sense
        # if we are running this code on GCP, because then this file cannot be accessed once the code finished its execution)
        joblib.dump(self.model, local_model_name)
        print("saved model.joblib locally")
        client = storage.Client().bucket(BUCKET_NAME)
        storage_location = f"models/{local_model_name}"
        blob = client.blob(storage_location)
        blob.upload_from_filename(local_model_name)
        print("uploaded model.joblib to gcp cloud storage under \n => {}".format(storage_location))

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

if __name__ == '__main__':

    ###################
    #
    # preparation datas
    #
    ####################
    df_data = Data_loading().get_data_from_gcp(local=True)

    encoder = Encoder(df_data)
    df_data = encoder.execute(col_name = 'nom_commune')
    encoder2 = Encoder(df_data)
    df_data = encoder2.execute(col_name = 'type_local')

    #selection des colonnes
    cols = list(df_data.columns)

    columns_todrop = ['id_mutation', 'date_mutation', 'nature_mutation',
            'adresse_nom_voie', 'adresse_code_voie',
    'code_commune', 'code_postal',
    'code_departement',
    'id_parcelle', 'Prixm2', 'longitude', 'latitude','prixmetre','Unnamed: 0', 'Unnamed: 0.1']


    for i in columns_todrop:
        cols.remove(i)

    cols_removd_target = cols[:]
    cols_removd_target.remove('valeur_fonciere') # target variables are removed

    # hard value for randomize search
    reg = 10
    forest = 10
    xgboost = 10

    randomsearch_dict = {"reg_iter": reg,
    "forest_iter": forest,
    "xgboost_iter": xgboost}

    ######################
    #
    #    RIDGE
    # Example of parameters for randomsearch for LASSO  model :**
    #
    ########################

    # params_cv_ridge = {'alpha': stats.norm(0.9,3) , "fit_intercept": [True, False], "solver": ['auto']}




    # traitement = Trainer(df_data, cols_removd_target, 'valeur_fonciere', RobustScaler(), 'Ridge', params_cv_ridge, randomsearch_dict)
    # result = traitement.execute()
    # print(result)
    # traitement.save_model_to_gcp('Ridge')

    ######################
    #
    #    LASSO
    # Example of parameters for randomsearch for LASSO  model :**
    #
    ########################

    params_cv_lasso = {'alpha': stats.norm(0,3) , "fit_intercept": [True], 'max_iter': [50000]}

    traitement = Trainer(df_data, cols_removd_target, 'valeur_fonciere', RobustScaler(), 'Lasso', params_cv_lasso, randomsearch_dict)
    result = traitement.execute()
    print(result)
    traitement.save_model_to_gcp('Lasso')


    ######################
    #
    #    RANDOM FOREST
    #
    ########################


    # n_estimators = [10, 15, 20, 25]
    #                                                                                     #in the random forest
    # max_features = ['sqrt', 'log2'] # number of features in consideration at every split
    # max_depth = [int(x) for x in np.linspace(10, 200, num = 5)] # maximum number of levels
    #                                                                         #allowed in each decision tree
    # min_samples_split = [0.1, 0.3, 0.5, 0.8] # minimum sample number to split a node
    # min_samples_leaf = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6] # minimum sample number that can be stored in a leaf node
    # min_impurity_decrease = [0.01, 0.1, 1, 5, 10]
    # bootstrap = [True, False] # method used to sample data points

    # params_cv_forest = {'n_estimators': n_estimators,
    #         'max_features': max_features,
    #         'max_depth': max_depth,
    #         'min_samples_split': min_samples_split,
    #         'min_samples_leaf': min_samples_leaf,
    #         'bootstrap': bootstrap,
    #         'min_impurity_decrease': min_impurity_decrease
    #         }

    # reg = 10
    # forest = 10
    # xgboost = 10

    # randomsearch_dict = {"reg_iter": reg,
    #                         "forest_iter": forest,
    #                         "xgboost_iter": xgboost}

    # traitement = Trainer(df_data, cols_removd_target, 'valeur_fonciere', RobustScaler(), 'RandomForest', params_cv_forest, randomsearch_dict)
    # result = traitement.execute()
    # print(result)
    # traitement.save_model_to_gcp('RandomForest')


    ######################
    #
    #    XGBOOST
    # Example of parameters for randomsearch for Randomforest model :**
    #
    ########################


    # n_estimators = [35, 40, 55]
    #                                                                                     #in the random forest
    # max_features = ['sqrt', 'log2'] # number of features in consideration at every split
    # max_depth = [int(x) for x in np.linspace(10, 200, num = 5)] # maximum number of levels
    #                                                                         #allowed in each decision tree
    # min_samples_split = [0.1, 0.3, 0.5, 0.8] # minimum sample number to split a node
    # min_samples_leaf = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6] # minimum sample number that can be stored in a leaf node
    # min_impurity_decrease = [0.01, 0.1, 1, 5, 10]
    # bootstrap = [True, False] # method used to sample data points

    # params_cv_forest = {'n_estimators': n_estimators,
    #         'max_features': max_features,
    #         'max_depth': max_depth,
    #         'min_samples_split': min_samples_split,
    #         'min_samples_leaf': min_samples_leaf,
    #         'bootstrap': bootstrap,
    #         'min_impurity_decrease': min_impurity_decrease
    #         }

    # reg = 10
    # forest = 10
    # xgboost = 10

    # randomsearch_dict = {"reg_iter": reg,
    #                       "forest_iter": forest,
    #                        "xgboost_iter": xgboost}

    # traitement = Trainer(df_data, cols_removd_target, 'Prixm2', RobustScaler(), 'XGBoost', params_cv_xgboost, randomsearch_dict)
    # traitement.execute()
    # traitement.save_model_to_gcp('XGBoost')
