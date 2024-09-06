import requests
import boto3
import pandas as pd
from io import StringIO

######################### Conection to AWS ######################

s3_bucket = 'climate-change-datalake'
s3_target_file_name = 'Raw/Sea-level-change/sea-level_fig-1.csv'
###############################################################

########## Read dataset csv from URL in a Pandas DataFrame ##########
data_url = 'http://www3.epa.gov/climatechange/images/indicator_downloads/sea-level_fig-1.csv'
response = requests.get(data_url)
df = pd.read_csv(StringIO(response.text))
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

print("Global Average Absolute Sea Level Change Data SUCCESFULLY uploaded to the S3 RAW zone")