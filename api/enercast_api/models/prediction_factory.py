from typing import Dict
from .prediction import Prediction
from time import time
from .utils import generate_id


class PredictionFactory:

    @staticmethod
    def create_default_prediction(prediction_parameters: Dict[str, str]) -> Prediction:
        time_submitted = str(time())
        time_completed = "-1"
        prediction_results = dict()
        id = generate_id()

        return Prediction(id,
                          time_submitted,
                          time_completed,
                          prediction_parameters,
                          prediction_results)
