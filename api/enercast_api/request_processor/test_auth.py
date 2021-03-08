from .auth import AuthContextProcessor
from ..models import AuthContext


def test_process_event() -> None:
    test_event = {
        "username": "vale"
    }
    processor = AuthContextProcessor()

    assert processor.process_event(test_event) == AuthContext(test_event["username"])
