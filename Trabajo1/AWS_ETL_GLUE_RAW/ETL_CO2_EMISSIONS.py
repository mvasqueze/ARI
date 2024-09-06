import requests
import zipfile
import io
import xml.etree.ElementTree as ET
import boto3

######################### Conection to AWS ######################

s3_bucket = 'climate-change-datalake'
s3_target_file_name = 'Raw/CO2-Emissions/CO2-Emissions.xml'
###############################################################

########## Step 1: Extract (Download and unzip the XML file) ##########
data_url = 'https://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.PC?downloadformat=xml'

response = requests.get(data_url)
# Verify respoonse
if response.status_code == 200:
    print("Response Status Code: 200")
    
    #  Unzip the ZIP file to memory
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # Show the list of files in the ZIP
        print("Files in ZIP:", z.namelist())
        
        # Extract file xml
        with z.open(z.namelist()[0]) as xml_file:
            xml_content = xml_file.read()  # Read content of the XML file

            ########## Step 2: Transform (Parse the XML file) ##########
            try:
                root = ET.fromstring(xml_content)
                print("XML parsed successfully.")

                xml_buffer = io.StringIO()
                xml_buffer.write(xml_content.decode('utf-8'))  

                ########## Step 3: Load (Upload to S3) ##########
                session = boto3.Session(
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    aws_session_token=aws_session_token
                )
                s3 = session.client('s3')

                # upload file
                s3.put_object(Body=xml_buffer.getvalue(), Bucket=s3_bucket, Key=s3_target_file_name)

                print("CO2 emissions Data SUCCESSFULLY uploaded to the S3 RAW zone")
            except ET.ParseError as e:
                print(f"Error parsing XML: {e}")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
