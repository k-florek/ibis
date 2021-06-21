import boto3

def upload_seqrun(data,aws=False):
    #try to connect to local db if dynamodb is not available
    if aws:
        dynamodb = boto3.resource('dynamodb',region_name='us-east-2')
    else:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('SC2')
    for sample in data.keys():
        print("Adding sample:", sample)
        table.put_item(Item=data[sample])
