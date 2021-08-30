"""
IMPORT PARAMETERS FOR MAKEFILE
"""
# ----------------------------------
#      GCP PARAMETERS (check which parameters to keep)
# ----------------------------------
PROJECT_ID= '<GCP Project Name>' # Name of the procject in GCP account
BUCKET_NAME='<GCP Bucket Name>'
BUCKET_FOLDER = 'Bucket folder'  # bucket directory in which to store the uploaded file
BUCKET_TRAIN_DATA_PATH='<BUCKET_TRAIN_DATA_PATH>'

REGION='europe-west1'
PYTHON_VERSION=3.7
FRAMEWORK='scikit-learn'
RUNTIME_VERSION=1.15
PACKAGE_NAME='reestimator'
FILENAME='<FILENAME>'

# ----------------------------------
#      JOB PARAMETERS (check which parameters to keep)
# ----------------------------------
JOB_NAME='<JOB_TO_DO>'
EXPERIMENT_NAME='<Experiment Name>'  # Name of MLFlow server

# ----------------------------------
#      DOCKER PARAMETERS (check which parameters to keep)
# ----------------------------------


# ----------------------------------
#      HEROKU PARAMETERS (check which parameters to keep)
# ----------------------------------


# ----------------------------------
#      PREDICT PARAMETERS (check which parameters to keep)
# ----------------------------------
MODEL_NAME = 'predict model name'
MODEL_VERSION = 'version of the model'
STORAGE_LOCATION = 'path location to model.joblib file'

# ----------------------------------
#      PACKAGE PARAMETERS (check which parameters to keep)
# ----------------------------------

PACKAGE_NAME=reestimator
FILENAME=trainer
