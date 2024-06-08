import json
import logging
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import time

logger = logging.getLogger()
logger.setLevel("INFO")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('merlin_messages')
client = boto3.client('dynamodb')

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

    transact_put_item(
        Item={
            'game': event['game'],
            'seq': seq,
            'id': payload['id'],
            'user.id': payload['user']['id'],
            'user.type': payload['user']['type'],
            'effect': json.dumps(payload['effect'])
        },
        ConditionExpression=Attr('game').not_exists(),
        ClientRequestToken=payload['id']
    )
    
def transact_put_item(Item, ConditionExpression, ClientRequestToken):
    client.transact_write_items(
        TransactItems=[
            {
                'Put': {
                    "TableName": "merlin_messages",
                    "Item": {
                        "game": {"S": Item['game']},
                        "seq": {"N": str(Item['seq'])},  # Assuming seq is a number
                        "id": {"S": Item['id']},
                        "user.id": {"N": str(Item['user.id'])},
                        "user.type": {"S": Item['user.type']},
                        "effect": {"S": Item['effect']}
                    },
                    "ConditionExpression": "attribute_not_exists(game)"
                }
            }
        ],
        ClientRequestToken=ClientRequestToken
    )
    
def retry_exc(exc):
    return exc.response['Error']['Code'] == 'ConditionalCheckFailedException'
