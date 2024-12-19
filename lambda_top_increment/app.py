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
    partition_index_name = os.environ['PARTITION_COUNTER_INDEX_NAME']
    partition_key = os.environ['PARTITION_COUNTER_INDEX_KEY']
    
    try:
        response = table.query(
            IndexName=partition_index_name,
            KeyConditionExpression=boto3.dynamodb.conditions.Key(partition_key).eq(partition_key),
            Limit=1,
            ScanIndexForward=False,
        )

        if response['Count'] == 0:
            return {
                'statusCode': 500,
                'headers': {"Content-Type": "application/json"},
                'body': json.dumps({'error': 'No items found'})
            }
        
        items = [
            {
                'userId': m['user_id'],
                'increments': decimal_to_int(m['counter'])
            }
            for m in response['Items']
        ]

        return {
            'statusCode': 200,
            'headers': {"Content-Type": "application/json"},
            'body': json.dumps(items[0])
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {"Content-Type": "application/json"},
            'body': json.dumps({'error': str(e)})
        }
