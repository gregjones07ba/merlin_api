import json
import logging

logger = logging.getLogger()
logger.setLevel("INFO")

def lambda_handler(event, context):
    logger.info(f"game: {event['game']}")
    
    result = {
        'messages': [
            {
                'userId': 12,
                'effect': {
                    'text': 'I cast Fireball!'
                }
            }
        ]
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
