from typing import Dict


class ContactUs:

    def __init__(self,
                 id: str,
                 time_submitted: str,
                 user_id: str,
                 subject: str,
                 message: str):
        self._id = id
        self._time_submitted = time_submitted
        self._user_id = user_id
        self._subject = subject
        self._message = message

    @property
    def id(self) -> str:
        return self._id

    @property
    def time_submitted(self) -> str:
        return self._time_submitted

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def subject(self) -> str:
        return self._subject

    @property
    def message(self, new_value: str) -> None:
        self._message = message

    def serialize(self) -> Dict[str, str]:
        return {
            "ID": self._id,
            "time_submitted": self._time_submitted,
            "user_id": self._user_id,
            "subject": self._subject,
            "message": self._message
        }

    @staticmethod
    def deserialize(serialized_data: Dict[str, str]):
        return Prediction(serialized_data["ID"],
                          serialized_data["time_submitted"],
                          serialized_data["user_id"],
                          serialized_data["subject"],
                          serialized_data["message"])

    def __eq__(self, other) -> bool:
        return (type(self) == type(other)) and \
               (self.serialize() == other.serialize())
