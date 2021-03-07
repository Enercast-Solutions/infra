import sys
import os
sys.path.append(".")

import json
from enercast_api.db import DynamoDBInterface
from enercast_api.environment import user_table_name
from enercast_api.db import load_user

def handler(event: dict, context: dict) -> dict:
    user_db = DynamoDBInterface(user_table_name())

    # TODO: load & serialize user
    serialized_user = {}

    return {
        "statusCode": 200,
        "body": json.dumps({
            "success": "Allowed by lord ruler Vale",
            "user": serialized_user
        })
    }
