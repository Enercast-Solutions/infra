from abc import abstractmethod
from abc import ABCMeta
from typing import Any


class AbstractProcessor(metaclass=ABCMeta):

    @abstractmethod
    def process_event(self, event: dict) -> Any:
        raise NotImplementedError("process_event() is not implemented")
