from reestimator.preprocessing.cleanup_data import Cleaning_data
#from reestimator.Mysql_mgmt.get_data import Data_loading
from reestimator.preproc_pipe import Preproc
import pandas as pd
from google.cloud import storage


# dataloader = Data_loading()
# df = dataloader.load_data_chunk('data_working_update', 100000)
# print("database chargée...\n")

def lancement_cleanin_local(df):
    cleaner = Cleaning_data(df)
    cleaner.cleaning()
    print("cleaning effectué...\n")
    prepr = Preproc(cleaner.df)
    final_df = prepr.preproc_pipe()
    print("préproc effectué...\n")
    final_df.to_csv('/media/jean/DATA/data_cleaned.csv')
    print("fichier écrit...\n")
    # dataloader.data_to_sql(final_df, 'data_cleaned', 'replace')
    # print("database écrite. Fin.")

​
@simple_time_tracker
def get_data_from_gcp(nrows='all', local=False, **kwargs):
    """method to get the training data (or a portion of it) from google cloud bucket"""
    # Add Client() here
    client = storage.Client()
    if local:
        path = "data/data_data_10Mill.csv"
    else:
        path = "gs://reestimator/"
        if nrows == 'all':
            df = pd.read_csv(path)
        else:
            df = pd.read_csv(path, nrows=nrows)
    return df
​
# def get_data(nrows=10_000):
#     '''returns a DataFrame with nrows from s3 bucket'''
#     df = pd.read_csv(AWS_BUCKET_PATH, nrows=nrows)
#     return df

# def clean_data(df, test=False):
#     df = df.dropna(how='any', axis='rows')
#     df = df[(df.dropoff_latitude != 0) | (df.dropoff_longitude != 0)]
#     df = df[(df.pickup_latitude != 0) | (df.pickup_longitude != 0)]
#     if "fare_amount" in list(df):
#         df = df[df.fare_amount.between(0, 4000)]
#     df = df[df.passenger_count < 8]
#     df = df[df.passenger_count >= 0]
#     df = df[df["pickup_latitude"].between(left=40, right=42)]
#     df = df[df["pickup_longitude"].between(left=-74.3, right=-72.9)]
#     df = df[df["dropoff_latitude"].between(left=40, right=42)]
#     df = df[df["dropoff_longitude"].between(left=-74, right=-72.9)]
#     return df

def lancement_cleaning_gcp(df):

    cleaner = Cleaning_data(df)
    cleaner.cleaning()
    prepr = Preproc(cleaner.df)
    final_df = prepr.preproc_pipe()


if __name__ = "__main__":
    df = get_data()
    lancement_cleaning_gcp(df)
