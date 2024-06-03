import json
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

def lambda_handler(event, context):
    logger.info(event)
    
    return {
        'messages': [
            {
                'id': 'abcd1234-dcba-4321-abcd-1234dcba4321',
                'seq': 0,
                'user': {
                    'id': 12,
                    'type': 'player'
                },
                'effect': {
                    'text': 'I cast Fireball!'
                }
            }
        ]
    }
