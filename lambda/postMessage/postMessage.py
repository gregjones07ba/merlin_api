import json
import logging
import boto3
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('merlin_messages')

def lambda_handler(event, context):
    logger.info(event)

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
    
    table.put_item(Item={
        'game': event['game'],
        'seq': seq,
        'id': payload['id'],
        'user.id': payload['user']['id'],
        'user.type': payload['user']['type'],
        'effect': json.dumps(payload['effect'])
    })
    
    return {
    }
