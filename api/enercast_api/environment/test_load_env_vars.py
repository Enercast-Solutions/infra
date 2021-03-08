import os
from .load_env_vars import user_table_name, prediction_service_endpoint


def test_user_table_name_pass() -> None:
    val = "HELLOWORLD"
    os.environ["USER_TABLE_NAME"] = val

    assert user_table_name() == val


def test_prediction_service_endpoint_pass() -> None:
    val = "HELLO"
    os.environ["PREDICTION_SERVICE_ENDPOINT"] = val

    assert prediction_service_endpoint() == val
