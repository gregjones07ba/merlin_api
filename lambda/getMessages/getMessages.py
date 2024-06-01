import json

def lambda_handler(event, context):
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
