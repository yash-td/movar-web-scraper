"""
Simple test function to verify Netlify Python functions are working
"""

import json


def handler(event, context):
    """Simple test handler"""

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'success': True,
            'message': 'Python functions are working!',
            'event': event.get('httpMethod', 'unknown')
        })
    }
