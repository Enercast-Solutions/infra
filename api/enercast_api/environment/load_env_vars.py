import os

USER_TABLE_NAME_ENV_VAR = "USER_TABLE_NAME"
PREDICTION_SERVICE_ENDPOINT = "PREDICTION_SERVICE_ENDPOINT"


def user_table_name() -> str:
    return os.environ[USER_TABLE_NAME_ENV_VAR]


def prediction_service_endpoint() -> str:
    return os.environ[PREDICTION_SERVICE_ENDPOINT]
