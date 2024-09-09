import requests
import zipfile
import io
import xml.etree.ElementTree as ET
import boto3
import pandas as pd

######################### Conection to AWS ######################
s3_bucket = 'climate-change-datalake'
s3_target_file_name = 'Raw/CO2-Emissions/CO2-Emissions.xml'

## Credentials ##

###############################################################

########## Step 1: Extract (Download and unzip the XML file) ##########
data_url = 'https://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.PC?downloadformat=xml'

response = requests.get(data_url)
# Verify response
if response.status_code == 200:
    print("Response Status Code: 200")
    
    #  Unzip the ZIP file to memory
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        print("Files in ZIP:", z.namelist())
        
        # Extract the XML file
        with z.open(z.namelist()[0]) as xml_file:
            xml_content = xml_file.read()  

            ########## Step 2: Transform ##########
            try:
                root = ET.fromstring(xml_content)
                print("XML parsed successfully.")

                # Create a list to hold parsed records
                records = []
                for record in root.findall(".//record"):
                    record_data = {}
                    for field in record.findall(".//field"):
                        field_name = field.attrib.get('name')
                        field_value = field.text
                        record_data[field_name] = field_value
                    records.append(record_data)
                df = pd.DataFrame(records)

                ########## Step 3: Load (Upload to S3 as CSV) ##########
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)

                session = boto3.Session(
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    aws_session_token=aws_session_token
                )
                s3 = session.client('s3')
                s3.put_object(Body=csv_buffer.getvalue(), Bucket=s3_bucket, Key=s3_target_file_name)

                print(f"CO2 emissions data successfully uploaded to {s3_target_file_name} in the S3 RAW zone as CSV.")
            except ET.ParseError as e:
                print(f"Error parsing XML: {e}")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
