#Load Libraries and Create engine Connection

import pymysql
import pandas as pd
import numpy as np
import sqlalchemy
import gc
engine =sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
        drivername="mysql+pymysql",
        username='Estimators',  # e.g. "my-database-user"
        password='Estimator2021',  # e.g. "my-database-password"
        host='34.77.88.127',  # e.g. "127.0.0.1"
        port=3306,  # e.g. 3306
        database='Housing_France',  # e.g. "my-database-name"
    ))

conn = engine.connect().execution_options(stream_results=True)    

class dloading  :
#Load Libraries and Create engine Connection

    def load_data_chunk(table_name,chunksize):

        frame = pd.DataFrame()
        for chunk_dataframe in pd.read_sql(
                f"""Select * from {table_name}""", conn, chunksize=chunksize):
                print(f"Got dataframe w/{len(chunk_dataframe)} rows")
                frame= frame.append(chunk_dataframe)
        
        return frame

    def get_random_rows(table_name, numrows):
        conn = engine.connect().execution_options(stream_results=True)
        df = pd.read_sql(f"""SELECT * FROM {table_name} dm ORDER BY RAND() LIMIT {numrows};""",conn)
        return df

    def get_all_rows(table_name):
        df = pd.read_sql(f"""SELECT * FROM {table_name} """,conn)
        return df

    def get_num_rows(table_name, rownums):
        df = pd.read_sql(f"""SELECT * FROM {table_name} Limit {rownums} """, conn)
        return df
    
    def show_tables():
        engine2 =sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
        drivername="mysql+pymysql",
        username='Estimators',  # e.g. "my-database-user"
        password='Estimator2021',  # e.g. "my-database-password"
        host='34.77.88.127',  # e.g. "127.0.0.1"
        port=3306,  # e.g. 3306
        database='Housing_France',  # e.g. "my-database-name"
        ))
        conn2 = engine.connect().execution_options(stream_results=True)
        df = pd.read_sql("""SELECT TABLE_NAME FROM information_schema.tables where TABLE_SCHEMA = 'Housing_France'""",conn2)
        return df

    def data_to_sql(df, tablename, if_exists):
        """Export Data to Sql, if exists takes one of the two strings :  ['replace','append'] """
        df.to_sql(name=f'{str(tablename)}', con=conn, if_exists=f'{if_exists}', index=True)
        return print(f"the table {str(tablename)} was successfully loaded to DB")

print(dloading.get_num_rows('data',1000))
print(dloading.show_tables())