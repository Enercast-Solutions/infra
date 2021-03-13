from typing import List
from .prediction import Prediction


class User:

    def __init__(self,
                 id: str,
                 cc_info: dict,
                 energy_consumption_predictions: List[Prediction]):
        self._id = id
        self._cc_info = cc_info
        self._energy_consumption_predictions = energy_consumption_predictions

    @property
    def id(self) -> str:
        return self._id

    @property
    def cc_info(self) -> dict:
        return self._cc_info

    @cc_info.setter
    def cc_info(self, new_cc_info: dict) -> None:
        self._cc_info = new_cc_info

    @property
    def energy_consumption_predictions(self) -> List[Prediction]:
        return self._energy_consumption_predictions

    def add_prediction(self, new_prediction: Prediction) -> None:
        self._energy_consumption_predictions.append(new_prediction)

    def serialize(self) -> dict:
        return {
            "ID": self._id,
            "cc_info": self._cc_info,
            "energy_consumption_predictions": self.serialize_predictions()
        }

    def serialize_predictions(self) -> List[dict]:
        return [pred.serialize() for pred in self._energy_consumption_predictions]

    @staticmethod
    def deserialize(serialized_data: dict):
        return User(serialized_data["ID"],
                    serialized_data["cc_info"],
                    User.deserialize_predictions(serialized_data["energy_consumption_predictions"]))

    @staticmethod
    def deserialize_predictions(serialized_data: List[dict]) -> List[Prediction]:
        return [Prediction.deserialize(pred) for pred in serialized_data]

    def __eq__(self, other) -> bool:
        return (type(self) == type(other)) and \
               (self.serialize() == other.serialize())
