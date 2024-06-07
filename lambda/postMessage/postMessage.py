import json
import logging
import boto3
from boto3.dynamodb.conditions import Key, Attr
import time

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('merlin_messages')

def lambda_handler(event, context):
    logger.info(event)

    add_message(event)

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
        
    time.sleep(10)
    
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
