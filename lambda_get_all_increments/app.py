import json
import boto3
import os

def lambda_handler(event, context):
    # Get all increments
    dynamodb = boto3.resource('dynamodb')
    tableName = os.environ['DYNAMODB_TABLE_NAME']
    table = dynamodb.Table(tableName)

    try:
        response = table.scan()
        items = response['Items']
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                'increments': items
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }