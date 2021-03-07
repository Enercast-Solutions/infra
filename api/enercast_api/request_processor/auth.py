from .abstract import AbstractProcessor


class AuthProcessor(AbstractProcessor):

    def process_event(self, event: dict) -> str:
        return event["username"]
