from abc import abstractmethod
from abc import ABC
from typing import Any


class AbstractProcessor(ABC):

    @abstractmethod
    def process_event(self, event: dict) -> Any:
        raise NotImplementedError("process_event() is not implemented")
