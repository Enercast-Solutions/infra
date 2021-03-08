from abc import ABC
from abc import abstractmethod


class AbstractController(ABC):

    @abstractmethod
    def execute(self) -> dict:
        raise NotImplementedError("execute() not implemented")
