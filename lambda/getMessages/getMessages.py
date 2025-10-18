import json
import logging
from os import environ

import boto3
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(environ['MESSAGES_TABLE'])

def lambda_handler(event, context):
    logger.info(event)
    
    game = event['game']
    start_str = event['start']
    end_str = event['end']
    
    start = int(start_str) if start_str else None
    end = int(end_str) if end_str else None
    
    key_condition = Key('game').eq(event['game'])
    if start is not None and end is not None:
        key_condition = key_condition & Key('seq').between(start, end)
    elif start is not None:
        key_condition = key_condition & Key('seq').gt(start)
    elif end is not None:
        key_condition = key_condition & Key('seq').lt(end)
    
    response = table.query(
        KeyConditionExpression = key_condition,
        Limit = 10,
        ScanIndexForward = False
    )
    
    return {
        'messages': [
            transform(item)
            for item in response['Items']
            if include(item, start, end)
        ]
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
    
def include(message_item, start, end):
    # must enforce in code because the between key condition cannot be an exclusive range
    return (
        (start is None or start < message_item['seq']) and
        (end is None or message_item['seq'] < end)
    )
