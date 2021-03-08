from .prediction_factory import PredictionFactory


def test_create_default_prediction_pass() -> None:
    prediction_parameters = {
        "testing_num": "123124",
        "rooms": "10"
    }

    prediction = PredictionFactory.create_default_prediction(prediction_parameters)

    assert prediction.prediction_parameters == prediction_parameters
    assert prediction.time_completed == "-1"
    assert prediction.prediction_results == dict()
    assert type(prediction.id) == str
    assert prediction.time_submitted != "-1"
