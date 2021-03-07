from abc import abstractmethod
from abc import ABC


class DB(ABC):

    @abstractmethod
    def create_or_update(self, id: str, obj: dict) -> None:
        raise Exception("create_or_update_object() not implemented")

    @abstractmethod
    def delete(self, id: str) -> None:
        raise Exception("delete_object() not implemented")

    @abstractmethod
    def get(self, id: str) -> dict:
        raise Exception("get_object() not implemented")
