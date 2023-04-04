import os
import json
import boto3


dynamodb = boto3.resource('dynamodb', endpoint_url=os.environ['AWS_ENDPOINT_URL'])


def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps(result['Item'])
    }

