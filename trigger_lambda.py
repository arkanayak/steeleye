""" This will invoke the lambda namely SteelEye """
import boto3
import json

client = boto3.client('lambda')
data = {}
response = client.invoke(FunctionName='SteelEye',
                         InvocationType='RequestResponse',
                         Payload=json.dumps(data))

result = json.loads(response.get('Payload').read())
print(result)

