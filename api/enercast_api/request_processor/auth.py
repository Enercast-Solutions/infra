from .abstract import AbstractProcessor
from ..models import AuthContext


class AuthContextProcessor(AbstractProcessor):

    def process_event(self, event: dict) -> AuthContext:
        # TODO: Need to get the identity information based on what Cognito passes the Lambda function
        return AuthContext(event["username"])
