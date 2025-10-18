import json
import logging
from os import environ
import time

import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(environ['MESSAGES_TABLE'])

def lambda_handler(event, context):
    logger.info(event)

    for retry in (0.2, 0.5, 1.0, None):
        try:
            add_message(event)
            break
        except ClientError as exc:
            if not retry_exc(exc) or retry is None:
                raise
            else:
                time.sleep(retry)

    return {
    }
    
def add_message(event):
    payload = event['payload']
    
    response = table.query(
        KeyConditionExpression = Key('game').eq(event['game']),
        Limit = 1,
        ScanIndexForward = False
    )
    if response['Items']:
        item = response['Items'][0]
        seq = item['seq'] + 1
    else:
        seq = 0

    table.put_item(
        Item={
            'game': event['game'],
            'seq': seq,
            'id': payload['id'],
            'user.id': payload['user']['id'],
            'user.type': payload['user']['type'],
            'effect': json.dumps(payload['effect'])
        },
        ConditionExpression=Attr('game').not_exists()
    )
    
def retry_exc(exc):
    return exc.response['Error']['Code'] == 'ConditionalCheckFailedException'
