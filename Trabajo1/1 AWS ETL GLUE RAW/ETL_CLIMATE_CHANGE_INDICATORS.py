import os
import boto3
import pandas as pd
from io import StringIO
import zipfile

######################### Kaggle API Credentials ######################
kaggle_username = '_____'
kaggle_key = '______'

# Set Kaggle environment variables
os.environ['_______'] = kaggle_username
os.environ['________'] = kaggle_key
#######################################################################

######################### Conection to AWS ######################

s3_bucket = 'climate-change-datalake'
s3_target_file_name = 'Raw/Climate-Change-Indicators/climate_change_indicators.csv'
###############################################################

########## Download dataset using Kaggle API ##########
# Define the Kaggle command to download the dataset
os.system('kaggle datasets download -d tarunrm09/climate-change-indicators --unzip')

# Load the CSV file into pandas DataFrame
df = pd.read_csv('climate_change_indicators.csv')
###############################################################

########### Transform DataFrame to CSV to send to S3 ###########
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
#########################################################################################

############ Send data to S3 ########################################################
session = boto3.Session(aws_access_key_id, aws_secret_access_key, aws_session_token)
s3 = session.client('s3')
s3.put_object(Body=csv_buffer.getvalue(), Bucket=s3_bucket, Key=s3_target_file_name)
#########################################################################################

print("Climate Change Indicators Data SUCCESSFULLY uploaded to the S3 RAW zone")
