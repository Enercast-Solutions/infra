import sys
import os
sys.path.append(".")

import json
from enercast_api.db import DynamoDBInterface
from enercast_api.environment import contact_us_requests_table_name
from enercast_api.db import load_user
from enercast_api.request_processor import AuthContextProcessor, ContactUsProcessor
from enercast_api.controllers.user import ContactUsController


def handler(event: dict, context: dict) -> dict:
    user_db = DynamoDBInterface(contact_us_requests_table_name())

    auth_context = AuthContextProcessor().process_event(event)

    contact_us_data = ContactUsProcessor().process_event(json.loads(event["body"]))

    output = ContactUsController(user_db, auth_context, contact_us_data).execute()

    return {
        "statusCode": 200,
        "body": json.dumps(output)
    }
