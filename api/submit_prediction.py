import sys
import os
sys.path.append(".")

import time
from enercast_api.db import DynamoDBInterface
from enercast_api.environment import user_table_name
from enercast_api.db import load_user
from enercast_api.request_processor import AuthContextProcessor


def handler(event: dict, context: dict) -> dict:
    user_db = DynamoDBInterface(user_table_name())

    # TODO: load user from request, not hardcoded. Need to understand how Cognito passes identity
    #   information to lambda function from the authorizer.
    auth_context = AuthContextProcessor().process_event({"username": "vale"})

    # TODO: load prediction information from request

    time_submitted = str(time.time())

    # TODO: incorporate controller for submit prediction

    return {
        "statusCode": 200,
        "body": "{}"
    }
