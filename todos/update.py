import json
import time
import logging
import os
import boto3


dynamodb = boto3.resource('dynamodb', endpoint_url=os.environ['AWS_ENDPOINT_URL'])


def update(event, context):
    data = json.loads(event['body'])

    if 'text' not in data or 'checked' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the todo item.")

    timestamp = str(time.time())

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames={
          '#todo_text': 'text',
        },
        ExpressionAttributeValues={
          ':text': data['text'],
          ':checked': data['checked'],
          ':updatedAt': timestamp,
        },
        UpdateExpression='SET #todo_text = :text, '
                         'checked = :checked, '
                         'updatedAt = :updatedAt',
        ReturnValues='ALL_NEW',
    )

    print(result['Attributes'])

    return {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'])
    }
