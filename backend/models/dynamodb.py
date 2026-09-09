import os

import boto3
from dotenv import load_dotenv

load_dotenv()

MOCK_AWS = os.getenv("MOCK_AWS", "true").lower() == "true"
DYNAMODB_TABLE = os.getenv(
    "DYNAMODB_TABLE_NAME",
    "AnnaSetuStateTable"
)


class DynamoDBStore:
    """
    Low-level adapter for DynamoDB.

    When MOCK_AWS=true, data is stored in an in-memory dictionary so
    the application can run without AWS credentials.
    """

    def __init__(self):
        self.mock_store = {}

        if MOCK_AWS:
            self.table = None
        else:
            dynamodb = boto3.resource("dynamodb")
            self.table = dynamodb.Table(DYNAMODB_TABLE)

    def get_item(self, pk: str, sk: str = None):
        if MOCK_AWS:
            key = (pk, sk)
            return self.mock_store.get(key)

        key = {"PK": pk}

        if sk is not None:
            key["SK"] = sk

        response = self.table.get_item(Key=key)
        return response.get("Item")

    def put_item(self, item: dict):
        if "PK" not in item:
            raise ValueError("DynamoDB item must contain PK")

        if MOCK_AWS:
            key = (
                item["PK"],
                item.get("SK")
            )
            self.mock_store[key] = item
            return item

        self.table.put_item(Item=item)
        return item

    def delete_item(self, pk: str, sk: str = None):
        if MOCK_AWS:
            self.mock_store.pop((pk, sk), None)
            return

        key = {"PK": pk}

        if sk is not None:
            key["SK"] = sk

        self.table.delete_item(Key=key)

    def scan_items(self):
        """
        Return all items.

        Used primarily by the mock implementation and simple demo
        queries. Production code should prefer DynamoDB Query operations
        when possible.
        """
        if MOCK_AWS:
            return list(self.mock_store.values())

        response = self.table.scan()
        return response.get("Items", [])


db_store = DynamoDBStore()