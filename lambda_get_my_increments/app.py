import json
import boto3
import os
from decimal import Decimal

def decimal_to_int(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError("Type not serializable")

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['DYNAMODB_TABLE_NAME']
    table = dynamodb.Table(table_name)
    
    try:
        user_id = event.get('requestContext', {}).get('authorizer', {}).get('claims', {}).get('sub')
        
        if not user_id:
            return {
                'statusCode': 401,
                'body': json.dumps({'message': "User id is required"})
            }
        
        response = table.get_item(Key={'user_id': user_id})
        item = response.get('Item') 

        if item:
            # convert counter to int
            item['counter'] = decimal_to_int(item['counter'])
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({'userId': user_id, 'email': item['email'], 'increments': item['counter']}) 
            }
        else:
            return {
                "statusCode": 404,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({'message': "User not found"})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {"Content-Type": "application/json"},
            'body': json.dumps({'error': str(e)})
        }
