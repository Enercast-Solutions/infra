import json
from db import DynamoDBInterface
from environment import user_table_name

def handler(event, context):
    user_db = DynamoDBInterface(user_table_name())

    return {
        "statusCode": 200,
        "body": json.dumps({"success": "Allowed by lord ruler Vale"})
    }
