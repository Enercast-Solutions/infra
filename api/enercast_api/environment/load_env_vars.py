import os

USER_TABLE_NAME_ENV_VAR = "USER_TABLE_NAME"
PREDICTION_SERVICE_ENDPOINT = "PREDICTION_SERVICE_ENDPOINT"
CONTACT_US_REQUESTS_TABLE_NAME_ENV_VAR = "CONTACT_US_REQUESTS_TABLE_NAME"


def user_table_name() -> str:
    return os.environ[USER_TABLE_NAME_ENV_VAR]


def prediction_service_endpoint() -> str:
    return os.environ[PREDICTION_SERVICE_ENDPOINT]


def contact_us_requests_table_name() -> str:
    return os.environ[CONTACT_US_REQUESTS_TABLE_NAME_ENV_VAR]
