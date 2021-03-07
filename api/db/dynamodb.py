from .db import DB
import boto3


class DynamoDBInterface(DB):

    ID_KEY_NAME = "ID"

    def __init__(self, table_name: str):
        self.table = DynamoDBInterface.get_dynamodb_table(table_name)

    def create_or_update(self, id: str, obj: dict) -> None:
        return self.table.put_item(Item={
            DynamoDBInterface.ID_KEY_NAME: id,
            **obj
        })

    def delete(self, id: str) -> None:
        try:
            return self.table.delete_item(Key={
                DynamoDBInterface.ID_KEY_NAME: id
            })
        except KeyError:
            raise ValueError("Requested resource does not exist.")

    def get(self, id: str) -> dict:
        try:
            return self.table.get_item(Key={
                DynamoDBInterface.ID_KEY_NAME: id
            })["Item"]
        except KeyError:
            raise ValueError("Requested resource does not exist.")

    @staticmethod
    def get_dynamodb_table(table_name: str):
        return boto3.resource('dynamodb').Table(table_name)
