import requests
import boto3
import os


######################### Kaggle API Credentials ######################
kaggle_username = '_____'
kaggle_key = '______'

# Set Kaggle environment variables
os.environ['_______'] = kaggle_username
os.environ['________'] = kaggle_key
#######################################################################

######################### Conection to AWS ######################


s3_bucket = 'climate-change-datalake'
video_urls = [
    'https://www.kaggle.com/datasets/brsdincer/climate-change-video-set-nasa/0the5j_1.mp4',
    'https://www.kaggle.com/datasets/brsdincer/climate-change-video-set-nasa/nsceeu_1.mp4'
]
###############################################################

########## Download from URL and uploaded to S3 ##########
session = boto3.Session(aws_access_key_id, aws_secret_access_key, aws_session_token)
s3 = session.client('s3')

for url in video_urls:
    response = requests.get(url)
    file_name = url.split('/')[-1]
    s3_target_file_name = f'Raw/Climate-change-videos/{file_name}'

    s3.put_object(Body=response.content, Bucket=s3_bucket, Key=s3_target_file_name)

print("Climate Change Video data uploaded SUCCESFULLY to the S3 Raw zone")
