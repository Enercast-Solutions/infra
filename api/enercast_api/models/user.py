from typing import List


class User:

    def __init__(self,
                 id: str,
                 cc_info: dict,
                 energy_consumption_predictions: List[dict]):
        self._id = id
        self._cc_info = cc_info
        self._energy_consumption_predictions = energy_consumption_predictions

    @property
    def id(self) -> str:
        return self._id

    @property
    def cc_info(self) -> dict:
        return self._cc_info

    @property
    def energy_consumption_predictions(self) -> List[dict]:
        return self._energy_consumption_predictions

    def add_prediction(self, new_prediction: dict) -> None:
        self._energy_consumption_predictions.append(new_prediction)

    def serialize(self) -> dict:
        return {
            "ID": self._id,
            "cc_info": self._cc_info,
            "energy_consumption_predictions": self._energy_consumption_predictions
        }

    @staticmethod
    def deserialize(serialized_data: dict):
        return User(serialized_data["ID"],
                    serialized_data["cc_info"],
                    serialized_data["energy_consumption_predictions"])

    def __eq__(self, other) -> bool:
        return (type(self) == type(other)) and \
               (self.serialize() == other.serialize())
