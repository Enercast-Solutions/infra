from typing import Dict


class Prediction:

    def __init__(self,
                 id: str,
                 time_submitted: str,
                 time_completed: str,
                 prediction_parameters: Dict[str, str],
                 prediction_results: Dict[str, str]):
        self._id = id
        self._time_submitted = time_submitted
        self._time_completed = time_completed
        self._prediction_parameters = prediction_parameters
        self._prediction_results = prediction_results

    @property
    def id(self) -> str:
        return self._id

    @property
    def time_submitted(self) -> str:
        return self._time_submitted

    @property
    def time_completed(self) -> str:
        return self._time_completed

    @time_completed.setter
    def time_completed(self, new_value: str) -> None:
        self._time_completed = new_value

    @property
    def prediction_parameters(self) -> Dict[str, str]:
        return self._prediction_parameters

    @property
    def prediction_results(self) -> Dict[str, str]:
        return self._prediction_results

    @prediction_results.setter
    def prediction_results(self, new_value: Dict[str, str]) -> None:
        self._prediction_results = new_value

    def serialize(self) -> Dict[str, str]:
        return {
            "ID": self._id,
            "time_submitted": self._time_submitted,
            "time_completed": self._time_completed,
            "prediction_parameters": self._prediction_parameters,
            "prediction_results": self._prediction_results
        }

    @staticmethod
    def deserialize(serialized_data: Dict[str, str]):
        return Prediction(serialized_data["ID"],
                          serialized_data["time_submitted"],
                          serialized_data["time_completed"],
                          serialized_data["prediction_parameters"],
                          serialized_data["prediction_results"])

    def __eq__(self, other) -> bool:
        return (type(self) == type(other)) and \
               (self.serialize() == other.serialize())
