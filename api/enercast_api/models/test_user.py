from collections import namedtuple
from typing import Any
from .user import User
import time
import pytest


@pytest.fixture
def user_info() -> Any:
    id = "vale"
    cc_info = {
        "num_rooms" : "123",
        "sq_footage": "100000"
    }
    energy_consumption_predictions = [
        {
            "id": "123764532dsdfdfdasfd234dv4",
            "parameters": {
                "num_attendees": "1000",
                "num_rooms_occupied": "5"
            },
            "time_submitted": str(time.time()),
            "time_completed": str(time.time()),
            "energy_consumption_prediction": {
                "total_kwh": "100000"
            }
        }
    ]
    user = User(id, cc_info, energy_consumption_predictions)
    serialized_user = {
        "ID": id,
        "cc_info": cc_info,
        "energy_consumption_predictions": energy_consumption_predictions
    }

    UserInfo = namedtuple("UserInfo", "id cc_info energy_consumption_predictions user serialized_user")

    return UserInfo(id,
                    cc_info,
                    energy_consumption_predictions,
                    user,
                    serialized_user)


def test_serialize_pass(user_info) -> None:
    assert user_info.user.serialize() == user_info.serialized_user


def test_deserialize_pass(user_info) -> None:
    assert user_info.user == User.deserialize(user_info.serialized_user)


def test_equals_pass() -> None:
    user_1 = User("vale", {}, [])
    user_2 = User("jordan", {}, [])
    user_3 = User("vale", {}, [])
    user_4 = User("vale", {}, [{"id": "12312314sdfafd234"}])
    user_5 = User("vale", {"rooms": "1235"}, [{"id": "12312314sdfafd234"}])

    assert user_1 != user_2
    assert user_1 == user_3
    assert user_3 != user_4
    assert user_4 != user_5


def test_add_prediction(user_info) -> None:
    new_prediction = {
        "id": "kjhgfdsytrecvbn56432cy773dfs",
        "parameters": {
            "num_attendees": "10000",
            "num_rooms_occupied": "50"
        },
        "time_submitted": str(time.time()),
        "time_completed": str(time.time()),
        "energy_consumption_prediction": {
            "total_kwh": "10000000"
        }
    }

    user_info.user.add_prediction(new_prediction)

    user_info.serialized_user["energy_consumption_predictions"].append(new_prediction)

    assert user_info.user.serialize() == user_info.serialized_user
