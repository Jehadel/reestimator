# Import libraries
import pandas as pd


class Preprocessing_data:
    def __init__(self, df):
        self.df=df


    def conv_int(self,col):
        """
        Convert a column 'col' dtype (str, float, int)
        to the smallest type integer according to data
        """
        # to do : check if column mixed str (ex. '2A') and int. col.str.isnumeric()==False
        return pd.to_numeric(col, downcast='integer')


    def conv_downcast(self):
        """
        Downcast numeric dtypes in dataframe df to save memory
        """
        float_cols = self.df.select_dtypes('float').columns
        int_cols = self.df.select_dtypes('integer').columns

        self.df[float_cols] = self.df[float_cols].apply(pd.to_numeric, downcast='float')
        self.df[int_cols] = self.df[int_cols].apply(pd.to_numeric, downcast='integer')



    def conv_date(self, col):
        """
        Convert a date str column 'col' to datetime format YYYY-MM-DD
        """
        return pd.to_datetime(col, format='%Y-%m-%d')


    def drop_rows_of_specific_column(self, col_name):  #df dataframe
        """
        Drop rows of specific columns with Nan
        """
        mod_df = self.df.dropna(how='any', subset=[col_name])
        return mod_df


    # A REMPLACER PAR REQUETE SQL ??? A VOIR
    def remplacement_mutation(self):
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
        self.df['nature_mutation'] = self.df['nature_mutation'].replace(
            replacement_mutation_dict)

        return self.df


    def cadastral_sector(self):
        """
        Get secteur_cadastral from id_parcelle and add a column to df
        """
        self.df["secteur_cadastral"] = self.df["id_parcelle"].str.slice(5, 10)
        cad_sector = self.df["secteur_cadastral"]

        return cad_sector


    def filter_dependency(self, df, n_line='all'):
        """
        Filter the dependencies in type_local columns
        Parameters
        ----------
            df : intitial dataframe
            n_lines : 'all' or number of lines

        Returns
        -------
            Series with type_local filtered by dependency
            Think to downcast in int8 after filtered dependencies
        """

        df_gr = df.copy()
        print(df)
        print(df_gr)
        df_gr = df_gr['type_local'] == 'Dépendance'
        if n_line == 'all':
            df['Dependency'] = df.apply(
                lambda x: 1
                if x.id_mutation in df_gr.id_mutation.values else 0,
                axis=1)
            rslt_df = df[(self.df['type_local'] != 'Dépendance')]
            return rslt_df

        else:
            df['Dependency'] = df.head(n_line).apply(
                lambda x: 1
                if x.id_mutation in df_gr.id_mutation.values else 0,
                axis=1)
            rslt_df = df[(df['type_local'] != 'Dépendance')]
            return rslt_df

    def filter_dependency(self, df2, n_line='all'):
        """
        parameters
        ----------
            data: intitial dataframe

        returns
        -------
            series with type_local filtered by dependency (downcoast to int8)
        """


        df_gr = df2[df2['type_local'] == 'Dépendance']

        if n_line == 'all':
            df2['Dependency']=df2.apply(lambda x: 1 if x.id_mutation in df_gr.id_mutation.values else 0, axis=1)
            rslt_df = df2[(df2['type_local'] != 'Dépendance')]
            return rslt_df

        else:
            df2['Dependency']=df2.head(n_line).apply(lambda x: 1 if x.id_mutation in df_gr.id_mutation.values else 0, axis=1)
            rslt_df = df2[(df2['type_local'] != 'Dépendance')]
            return rslt_df
