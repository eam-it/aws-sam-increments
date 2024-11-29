import json
import boto3
import os

def lambda_handler(event, context):
    # Step 1 - Update table
    dynamodb = boto3.resource('dynamodb')
    tableName = os.environ['DYNAMODB_TABLE_NAME']
    table = dynamodb.Table(tableName)

    try:
        user_id = event['requestContext']['authorizer']['claims']['sub']

        increment_item = table.get_item(Key={'user_id': user_id})
        if 'Item' in increment_item:
            item = increment_item['Item']
        else:
            item = {'message': 'User not found'}

        table.put_item(Item={
            'user_id': user_id,
            'counter': item.get('counter', 0) + 1
        })
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }

    # Step 2 - Send the "new increment" event to the SQS queue
    queueUrl = os.environ['QUEUE_URL']
    queue = boto3.client('sqs')
    queue.send_message(
        QueueUrl=queueUrl,
        DelaySeconds=2,
        MessageBody=("new increments")
    )

    # Step 3 - Return the response
    return { "statusCode": 200 }
