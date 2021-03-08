from .abstract import AbstractProcessor


class PredictionParametersProcessor(AbstractProcessor):

    PREDICTION_PARAMETERS_KEY = "prediction_parameters"

    def process_event(self, event: dict) -> dict:
        return event[PredictionParametersProcessor.PREDICTION_PARAMETERS_KEY]
