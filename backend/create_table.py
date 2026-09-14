import os
import boto3
from dotenv import load_dotenv

# Load credentials from the root .env
load_dotenv(dotenv_path=".env")

dynamodb = boto3.resource('dynamodb', region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
table_name = 'AnnaSetuStateTable'

try:
    print(f"Creating DynamoDB table: {table_name}...")
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'PK', 'KeyType': 'HASH'},
            {'AttributeName': 'SK', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'PK', 'AttributeType': 'S'},
            {'AttributeName': 'SK', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    print("Table created successfully! You can now run the backend.")
except Exception as e:
    # If the table already exists, it will throw a ResourceInUseException which is fine
    print(f"Result: {e}")
