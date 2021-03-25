import sys
import os
sys.path.append(".")

import json
from enercast_api.db import DynamoDBInterface
from enercast_api.environment import user_table_name
from enercast_api.db import load_user
from enercast_api.request_processor import AuthContextProcessor, PredictionParametersProcessor
from enercast_api.controllers.user import SubmitPredictionController


def handler(event: dict, context: dict) -> dict:
    user_db = DynamoDBInterface(user_table_name())

    auth_context = AuthContextProcessor().process_event(event)

    prediction_parameters = PredictionParametersProcessor().process_event(json.loads(event["body"]))

    output = SubmitPredictionController(user_db, auth_context, prediction_parameters).execute()

    return {
        "statusCode": 200,
        "body": json.dumps(output)
    }
