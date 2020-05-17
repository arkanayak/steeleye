""" This script will show the list of files generated in bucket arkas3b"""
from boto3 import client

bucket = 'arkas3b'
conn = client('s3')
for key in conn.list_objects(Bucket=bucket)['Contents']:
    print(key['Key'])
