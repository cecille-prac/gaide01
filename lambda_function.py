import json
from search-suspicious-party import *

def lambda_handler(event, context):

    # apiPath should match the path specified in action group schema
    if event['apiPath'] == '/get-receiving-entity-details':
        # Extract the property from request data
        start_url = get_named_property(event, 'start_url')

        scraped_text = get_receiving_entity_from_url(start_url)

        action_response = {
            'actionGroup': event['actionGroup'],
            'apiPath': event['apiPath'],
            'httpMethod': event['httpMethod'],
            'httpStatusCode': 200,
            'responseBody': {
                'application/json': {
                    'body': json.dumps({'scraped_text': scraped_text})
                }
            }
        }

        return {'response': action_response}

    # Return an error if apiPath is not recognized
    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'Invalid API path'})
    }

def get_named_property(event, name):
    return next(
        item for item in
        event['requestBody']['content']['application/json']['properties']
        if item['name'] == name
    )['value']
