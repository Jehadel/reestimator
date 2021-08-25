# Import libraries
import pandas as pd


class Preprocessing_data:
    def __init__(self) -> None:
        pass

    def conv_int(col):
        """
        Convert a column 'col' dtype (str, float, int)
        to the smallest type integer according to data
        """
        # to do : check if column mixed str (ex. '2A') and int. col.str.isnumeric()==False
        return pd.to_numeric(col, downcast='integer')


    def conv_downcast(df):
        """
        Downcast numeric dtypes in dataframe df to save memory
        """
        float_cols = df.select_dtypes('float').columns
        int_cols = df.select_dtypes('integer').columns

        df[float_cols] = df[float_cols].apply(pd.to_numeric, downcast='float')
        df[int_cols] = df[int_cols].apply(pd.to_numeric, downcast='integer')
        return df

    def conv_date(col):
        """
        Convert a datestr column 'col' to datetime format YYYY-MM-DD
        """
        return pd.to_datetime(col, format='%Y-%m-%d')

    def drop_rows_of_specific_column(df, col_name): #df dataframe
        """
        Drop rows of specific columns with Nan
        """
        mod_df = df.dropna( how='any',
                    subset=[col_name])
        return mod_df

    # A REMPLACER PAR REQUETE SQL ???
    def remplacement_mutation(df):
        """
        Remplace Sale by 1 and Others type of mutation data by 0 in nature_mutation column of df
        """

        replacement_mutation_dict = {
            'Vente': "1",
            'Vente terrain à bâtir': "0",
            'Echange': "0",
            "Vente en l'état futur d'achèvement": "0",
            'Adjudication': "0",
            'Expropriation': "0"
        }
        df['nature_mutation'] = df['nature_mutation'].replace(replacement_mutation_dict)

        return df

    def cadastral_sector(df):
        """
        Get secteur_cadastral from id_parcelle and add a column to df
        """
        df["secteur_cadastral"]= df["id_parcelle"].str.slice(5, 10)

        return df
