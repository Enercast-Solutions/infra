from .abstract import AbstractProcessor
from ..models import AuthContext


class AuthContextProcessor(AbstractProcessor):

    def process_event(self, event: dict) -> AuthContext:
        return AuthContext(event["requestContext"]["authorizer"]["jwt"]["claims"]["username"])
