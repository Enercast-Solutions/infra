from ..abstract import AbstractController
from ...db import DB, load_user
from ...models import AuthContext, PredictionFactory, User, Prediction
import requests
from typing import Dict
from ...environment import prediction_service_endpoint


class SubmitPredictionController(AbstractController):

    def __init__(self,
                 user_db: DB,
                 auth_context: AuthContext,
                 prediction_parameters: Dict[str, str]):
        self._user_db = user_db
        self._auth_context = auth_context
        self._prediction_parameters = prediction_parameters

    def call_prediction_service(self, user: User, prediction: Prediction) -> str:
        request_data = {
            "start_date": prediction.prediction_parameters["start_date"],
            "end_date": prediction.prediction_parameters["end_date"],
            "setup_days": prediction.prediction_parameters["setup_days"],
            "teardown_days": prediction.prediction_parameters["teardown_days"],
            "sqft": user.cc_info["sqft"],
            "forecast_attendance": prediction.prediction_parameters["forecast_attendance"],
            "is_audio": prediction.prediction_parameters["is_audio"],
        }

        url = f"http://{prediction_service_endpoint()}/energy_consumption_prediction"
        response = requests.post(url, json=request_data)

        return response.json()

    def execute(self) -> None:
        user = load_user(self._user_db, self._auth_context.id)

        prediction = PredictionFactory.create_default_prediction(self._prediction_parameters)
        prediction.prediction_results = self.call_prediction_service(user, prediction)

        user.add_prediction(prediction)

        self._user_db.create_or_update(user.id, user.serialize())
