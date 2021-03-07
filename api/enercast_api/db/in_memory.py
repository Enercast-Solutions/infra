from .db import DB


class InMemoryDBInterface(DB):

    def __init__(self):
        self.data = {}

    def create_or_update(self, id: str, obj: dict) -> None:
        self.data[id] = obj

        return True

    def delete(self, id: str) -> None:
        if id not in self.data:
            raise ValueError()

        del self.data[id]

    def get(self, id: str) -> dict:
        if id not in self.data:
            raise ValueError()

        return self.data[id]
