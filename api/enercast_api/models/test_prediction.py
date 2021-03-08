from .prediction import Prediction
from .prediction_factory import PredictionFactory


def test_serialize_pass(prediction_info) -> None:
    assert prediction_info.prediction.serialize() == prediction_info.serialized_prediction


def test_deserialize_pass(prediction_info) -> None:
    assert prediction_info.prediction == Prediction.deserialize(prediction_info.serialized_prediction)


def test_equals_pass() -> None:
    prediction_1 = PredictionFactory.create_default_prediction(dict())
    prediction_2 = PredictionFactory.create_default_prediction({
        "test_param_1": "lkjdlkfalsjkdfs"
    })
    prediction_3 = PredictionFactory.create_default_prediction(dict())

    # We force set some attrs so that we can ensure that the comparison is on the data
    prediction_3._id = prediction_1.id
    prediction_3._time_submitted = prediction_1.time_submitted

    assert prediction_1 != prediction_2
    assert prediction_1 == prediction_3
