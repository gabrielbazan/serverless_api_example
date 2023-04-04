import os
import boto3


dynamodb = boto3.resource('dynamodb', endpoint_url=os.environ['AWS_ENDPOINT_URL'])


def delete(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    table.delete_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    return {
        "statusCode": 204,
        "body": "",
    }
