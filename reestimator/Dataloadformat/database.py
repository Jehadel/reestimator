# Create Functions to load and push heavy datasets a sqlite database

#Load all datasets as frames
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import gc

import sqlalchemy

class data_loading:
    #Create a Sql engine to work with
    def __init__(self):
        self.engine =  create_engine('sqlite:///HousesFrance2.sqlite3', echo=True)
        self.conn =  self.engine.connect()

    def data_load(self, year):
        """Function to load and initially format our data - especialy empty columns"""
        df =pd.read_csv(f'rawdata/{str(year)}.gz', compression='gzip')
        columns = ['ancien_nom_commune','ancien_id_parcelle','ancien_code_commune','lot5_surface_carrez','lot4_surface_carrez','lot5_numero'
            ,'lot3_surface_carrez', 'numero_volume','lot4_numero','lot3_numero','adresse_suffixe']
        df.drop(columns=columns, inplace=True)
        print("loaded and formatted")
        return df

    def data_to_sql(conn, df, year):
        """Export Data to Sql"""
        df.to_sql(name=f'Houses_France_{str(year)}', con=conn, if_exists='replace', index=True)
        return print(f"year {str(year)} loaded to DB")

    def process_sql_using_pandas(self, query_string, chunk):
        """Load in chunksizes"""
        engine = create_engine('sqlite:///HousesFrance.sqlite3', echo=True)
        conn = engine.connect().execution_options(
            stream_results=True)

        for chunk_dataframe in pd.read_sql(
                query_string, conn, chunksize=chunk):
            print(f"Got dataframe w/{len(chunk_dataframe)} rows")
            # ... do something with dataframe ...
    def read_query(conn, query_string):
        """Read a random query and return a df"""
        query = query_string
        df = pd.read_sql(query, conn)
        return df


    def format_data(conn, year):
        df = data_loading.read_query(conn, f"""Select * from Houses_France_{year} """)
        columns = df.select_dtypes(include=['float']).drop(columns=['longitude', 'latitude'], axis=1).columns.to_list()
        columns2 = df.select_dtypes(include=['integer']).columns.to_list()
        columns3 =['nature_culture', 'nature_culture_speciale', 'surface_terrain','code_type_local',
                'type_local', 'surface_reelle_bati', 'nombre_pieces_principales','lot1_numero',
                'lot1_surface_carrez', 
                    'lot2_numero', 'lot2_surface_carrez']
        for i in columns:
            df[i]= pd.to_numeric(df[i], downcast='float')
        for b in columns2:
            df[b]= pd.to_numeric(df[b], downcast='integer')
        df.dtypes
        for i in columns3:
            df = df[(~df.duplicated()) | (df[i].isnull())]
        data_loading.data_to_sql(conn,df,year)
        return print("success in reformatting data table")

if __name__ == "__main__":
    years = [2019,2018,2017,2016]
    for i in years:
        df = data_load(i)
        data_to_sql(df,i)
        #df =process_sql_using_pandas()
        del df
        gc.collect()


create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
    sqlalchemy.engine.url.URL.create(
        drivername="mysql+pymysql",
        username='root',  # e.g. "my-database-user"
        password='Juni1994',  # e.g. "my-database-password"
        host='34.77.88.127',  # e.g. "127.0.0.1"
        port=3306,  # e.g. 3306
        database='Housing_France',  # e.g. "my-database-name"
    ),
    **db_config
)