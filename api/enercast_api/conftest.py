from collections import namedtuple
import pytest
from typing import Any
from .models import PredictionFactory, User


@pytest.fixture
def prediction_info() -> Any:
    prediction_parameters = {
        "num_attendees": "1000",
        "num_rooms_occupied": "5"
    }
    prediction = PredictionFactory.create_default_prediction(prediction_parameters)
    serialized_prediction = {
        "ID": prediction.id,
        "prediction_parameters": prediction_parameters,
        "time_submitted": prediction.time_submitted,
        "time_completed": "-1",
        "prediction_results": dict()
    }

    PredictionInfo = namedtuple('PredictionInfo', 'prediction_parameters prediction serialized_prediction')

    return PredictionInfo(prediction_parameters,
                          prediction,
                          serialized_prediction)


@pytest.fixture
def user_info(prediction_info) -> Any:
    id = "vale"
    cc_info = {
        "num_rooms" : "123",
        "sq_footage": "100000"
    }
    energy_consumption_predictions = [
        prediction_info.prediction
    ]
    user = User(id, cc_info, energy_consumption_predictions)
    serialized_user = {
        "ID": id,
        "cc_info": cc_info,
        "energy_consumption_predictions": [
            prediction_info.prediction.serialize()
        ]
    }

    UserInfo = namedtuple("UserInfo", "id cc_info energy_consumption_predictions user serialized_user")

    return UserInfo(id,
                    cc_info,
                    energy_consumption_predictions,
                    user,
                    serialized_user)
