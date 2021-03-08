from .submit_prediction import SubmitPredictionController
from ...models import UserFactory, AuthContext, User
from ...db import InMemoryDBInterface


def test_execute_pass() -> None:
    user_db = InMemoryDBInterface()

    username = "vale"
    auth_context = AuthContext(username)
    prediction_parameters = {
        "num_attendees": "1000",
        "num_rooms_occupied": "5"
    }

    controller = SubmitPredictionController(user_db, auth_context, prediction_parameters)
    controller.execute()

    loaded_user = User.deserialize(user_db.get(username))

    assert len(loaded_user.energy_consumption_predictions) == 1
