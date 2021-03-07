from .auth import AuthProcessor


def test_process_event() -> None:
    test_event = {
        "username": "vale"
    }
    processor = AuthProcessor()

    assert processor.process_event(test_event) == test_event["username"]
