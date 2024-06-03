import json
import logging
import boto3

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('merlin_main')

def lambda_handler(event, context):
    logger.info(event)

    payload = event['payload']
    
    table.put_item(Item={
        'PK': f"GAME_{event['game']}",
        'SK': f"MESSAGE_{0}",
        'id': payload['id'],
        'user.id': payload['user']['id'],
        'user.type': payload['user']['type'],
        'effect': json.dumps(payload['effect'])
    })
    
    return {
    }
