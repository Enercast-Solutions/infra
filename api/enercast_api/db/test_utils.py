from .utils import load_user
from ..models import UserFactory
from .in_memory import InMemoryDBInterface


def test_load_user_pass_exists() -> None:
    db = InMemoryDBInterface()

    id = "vale"
    new_prediction = {
        "fjdssdlf": "sdfasdffssdf"
    }
    user = UserFactory.create_default_user(id)
    user.add_prediction(new_prediction)

    db.create_or_update(id, user.serialize())

    loaded_user = load_user(db, id)

    assert user == loaded_user

def test_load_user_pass_not_exists() -> None:
    db = InMemoryDBInterface()

    id = "vale"

    loaded_user = load_user(db, id)

    assert UserFactory.create_default_user(id) == loaded_user
