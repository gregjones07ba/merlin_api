import json
import logging
import boto3
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('merlin_main')

def lambda_handler(event, context):
    logger.info(event)
    
    game = event['game']
    start_str = event['start']
    end_str = event['end'] or None
    
    start = int(start_str) if start_str else None
    end = int(end_str) if end_str else None
    
    game_pk = f"GAME_{event['game']}"
    key_condition = Key('PK').eq(game_pk) & Key('SK').begins_with("MESSAGE_")
    if start:
        key_condition = key_condition & Key('SK').gt(f"MESSAGE_{start}")
    if end:
        key_condition = key_condition & Key('SK').lt(f"MESSAGE_{end}")
    
    response = table.query(
        KeyConditionExpression = key_condition,
        Limit = 10,
        ScanIndexForward = False
    )
    
    messages = [ transform(item) for item in response['Items'] ]
    
    return {
        'messages': messages
    }
    
def transform(message_item):
    seq = int(message_item['SK'][len('MESSAGE_'):])
    
    return {
        'id': message_item['id'],
        'seq': seq,
        'user': {
            'id': message_item['user.id'],
            'type': message_item['user.type']
        },
        'effect': json.loads(message_item['effect'])
    }
