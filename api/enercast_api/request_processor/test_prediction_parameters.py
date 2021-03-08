from .prediction_parameters import PredictionParametersProcessor


def test_process_event() -> None:
    test_event = {
        "prediction_parameters": {
            "rooms": "100"
        }
    }
    processor = PredictionParametersProcessor()

    assert processor.process_event(test_event) == test_event["prediction_parameters"]
