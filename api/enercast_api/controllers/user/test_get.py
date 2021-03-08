from .get import GetUserController
from ...models import UserFactory, AuthContext
from ...db import InMemoryDBInterface


def test_execute_pass() -> None:
    user_db = InMemoryDBInterface()
    event = {
        "username": "vale"
    }
    auth_context = AuthContext(event["username"])

    controller = GetUserController(user_db, auth_context)

    assert UserFactory.create_default_user(event["username"]).serialize() == controller.execute()
