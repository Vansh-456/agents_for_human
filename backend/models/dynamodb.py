import os
import boto3
from dotenv import load_dotenv

load_dotenv()

MOCK_AWS = os.getenv("MOCK_AWS", "true").lower() == "true"
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE_NAME", "AnnaSetuStateTable")

if not MOCK_AWS:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE)
else:
    dynamodb = None
    table = None

class DynamoDBStore:
    def __init__(self):
        self.mock_store = {}

    def get_item(self, pk: str, sk: str = None):
        if MOCK_AWS:
            key = f"{pk}#{sk}" if sk else pk
            return self.mock_store.get(key)
        else:
            key = {"PK": pk}
            if sk: key["SK"] = sk
            response = table.get_item(Key=key)
            return response.get('Item')

    def put_item(self, item: dict):
        if MOCK_AWS:
            pk = item.get('PK')
            sk = item.get('SK', 'PROFILE')
            key = f"{pk}#{sk}"
            self.mock_store[key] = item
        else:
            table.put_item(Item=item)

db_store = DynamoDBStore()
