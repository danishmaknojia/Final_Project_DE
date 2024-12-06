import pandas as pd
import logging
import boto3
from io import StringIO

# Initialize a session using Amazon S3
s3 = boto3.client('s3')
bucket_name = "cbb-data-engg"

response = s3.list_objects_v2(Bucket=bucket_name)
for obj in response.get('Contents', []):
    print(obj['Key'])
