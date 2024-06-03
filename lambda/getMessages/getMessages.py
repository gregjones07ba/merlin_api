import json
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

def lambda_handler(event, context):
    logger.info(event)
    
    return {
        'messages': [
            {
                'userId': 12,
                'effect': {
                    'text': 'I cast Fireball!'
                }
            }
        ]
    }
