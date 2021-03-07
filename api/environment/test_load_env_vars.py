import os
from .load_env_vars import user_table_name


def test_user_table_name() -> None:
    val = "HELLOWORLD"
    os.environ["USER_TABLE_NAME"] = val

    assert user_table_name() == val
