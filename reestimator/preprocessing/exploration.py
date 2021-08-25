# Import libraries
import pandas as pd


class Exploration_data:
    def __init__(self,df):
        self.df = df



    def get_float_columns(self):
        """
        Get float columns
        """
        list_floats = list(self.df.select_dtypes(include=['float64']).columns)
        return list_floats


    def get_int_columns(self):
        """
        Get integer columns
        """
        list_int = list(self.df.select_dtypes(include=['int64']).columns)
        return list_int


    def get_object_columns(self):
        """
        Get object columns
        """
        list_objects = list(self.df.select_dtypes(include=['O']).columns)
        return list_objects


    def get_count_of_missing_values(self):
        """
        Get count of missing values in DataFrame
        """
        missing_df = pd.DataFrame(self.df.isnull().sum().sort_values(ascending=False))
        return missing_df


    def get_columns_with_missing_values(self):  #df dataframe
        """
        Get columns with missing values
        """
        missing_df = self.get_count_of_missing_values()
        missing_data = missing_df[missing_df[0] !=0]
        return missing_data


    def get_columns_without_missing_values(self):  #df dataframe
        """
        Get columns with out missing values
        """
        missing_df = self.get_count_of_missing_values()
        clean_data = missing_df[missing_df[0] == 0]
        return clean_data


    def get_count_missing_vals_in_1column(self, col_name):  #df dataframe && col_name : name of column
        """
        Get columns with out missing values
        """
        missing_df = self.get_count_of_missing_values()
        return df.shape[0] - missing_df.loc[col_name][0]
