from .user import User
from .prediction_factory import PredictionFactory


def test_serialize_pass(user_info) -> None:
    assert user_info.user.serialize() == user_info.serialized_user


def test_deserialize_pass(user_info) -> None:
    assert user_info.user == User.deserialize(user_info.serialized_user)


def test_equals_pass() -> None:
    user_1 = User("vale", {}, [])
    user_2 = User("jordan", {}, [])
    user_3 = User("vale", {}, [])
    user_4 = User("vale", {}, [PredictionFactory.create_default_prediction({"id": "12312314sdfafd234"})])
    user_5 = User("vale", {"rooms": "1235"}, [PredictionFactory.create_default_prediction(dict())])

    assert user_1 != user_2
    assert user_1 == user_3
    assert user_3 != user_4
    assert user_4 != user_5


def test_add_prediction_pass(user_info, prediction_info) -> None:
    new_prediction = PredictionFactory.create_default_prediction({
        "num_attendees": "10000",
        "num_rooms_occupied": "50"
    })

    user_info.user.add_prediction(new_prediction)

    user_info.serialized_user["energy_consumption_predictions"].append(new_prediction.serialize())

    assert user_info.user.serialize() == user_info.serialized_user


def test_serialize_predictions_pass() -> None:
    pred_1 = PredictionFactory.create_default_prediction({"ID": "1"})
    pred_2 = PredictionFactory.create_default_prediction({"ID": "2"})
    pred_3 = PredictionFactory.create_default_prediction({"ID": "3"})

    user = UserFactory.create_default_user("vale")

    user.add_prediction(pred_1)
    user.add_prediction(pred_2)
    user.add_prediction(pred_3)

    correct_list_of_predictions = [
        pred_1.serialize(),
        pred_2.serialize(),
        pred_3.serialize()
    ]

    assert correct_list_of_predictions == user.serialize_predictions()


def test_serialize_predictions_pass() -> None:
    pred_1 = PredictionFactory.create_default_prediction({"ID": "1"})
    pred_2 = PredictionFactory.create_default_prediction({"ID": "2"})
    pred_3 = PredictionFactory.create_default_prediction({"ID": "3"})

    serialized_predictions = [
        pred_1.serialize(),
        pred_2.serialize(),
        pred_3.serialize()
    ]

    correct_list_of_deserialized_predictions = [
        pred_1,
        pred_2,
        pred_3
    ]

    assert correct_list_of_deserialized_predictions == User.deserialize_predictions(serialized_predictions)
