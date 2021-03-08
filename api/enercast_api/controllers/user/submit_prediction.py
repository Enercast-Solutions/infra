from ..abstract import AbstractController
from ...db import DB, load_user
from ...models import AuthContext, PredictionFactory
from typing import Dict


class SubmitPredictionController(AbstractController):

    def __init__(self,
                 user_db: DB,
                 auth_context: AuthContext,
                 prediction_parameters: Dict[str, str]):
        self._user_db = user_db
        self._auth_context = auth_context
        self._prediction_parameters = prediction_parameters

    def execute(self) -> dict:
        user = load_user(self._user_db, self._auth_context.id)

        prediction = PredictionFactory.create_default_prediction(self._prediction_parameters)

        # TODO: Call prediction service here

        user.add_prediction(prediction)

        # Sure, we're making a 2nd call to the DB...but who cares?
        self._user_db.create_or_update(user.id, user.serialize())

        return user.serialize()
