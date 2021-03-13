import sys
import os
sys.path.append(".")

import json
from enercast_api.db import DynamoDBInterface
from enercast_api.environment import user_table_name
from enercast_api.db import load_user
from enercast_api.request_processor import AuthContextProcessor, CCInfoProcessor
from enercast_api.controllers.user import SubmitCCInfoController


def handler(event: dict, context: dict) -> dict:
    user_db = DynamoDBInterface(user_table_name())

    # TODO: load user from request, not hardcoded. Need to understand how Cognito passes identity
    #   information to lambda function from the authorizer.
    auth_context = AuthContextProcessor().process_event({"username": "vale"})

    cc_info = CCInfoProcessor().process_event(json.loads(event["body"]))

    SubmitCCInfoController(user_db, cc_info, auth_context).execute()

    return {
        "statusCode": 200,
        "body": "{}"
    }
