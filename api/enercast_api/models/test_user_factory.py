from .user_factory import UserFactory
from .user import User


def test_create_default_user_pass() -> None:
    id = "vale"
    correct_user = User(id, {}, [])

    assert correct_user == UserFactory.create_default_user(id)
