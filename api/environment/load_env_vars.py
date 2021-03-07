import os

USER_TABLE_NAME_ENV_VAR = "USER_TABLE_NAME"


def user_table_name() -> str:
    return os.environ[USER_TABLE_NAME_ENV_VAR]
