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
    
    game = event['game']
    start_str = event['start']
    end_str = event['end']
    
    start = int(start_str) if start_str else None
    end = int(end_str) if end_str else None
    
    key_condition = Key('game').eq(event['game'])
    if start is not None:
        key_condition = key_condition & Key('seq').gt(start)
    elif end is not None:
        key_condition = key_condition & Key('seq').lt(end)
    
    response = table.query(
        KeyConditionExpression = key_condition,
        Limit = 10,
        ScanIndexForward = False
    )
    
    return {
        'messages': [ transform(item) for item in response['Items'] ]
    }
    
def transform(message_item):
    seq = message_item['seq']
    
    return {
        'id': message_item['id'],
        'seq': message_item['seq'],
        'user': {
            'id': message_item['user.id'],
            'type': message_item['user.type']
        },
        'effect': json.loads(message_item['effect'])
    }
