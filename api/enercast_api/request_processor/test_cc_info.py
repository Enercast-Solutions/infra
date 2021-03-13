from .cc_info import CCInfoProcessor
from ..models import ConventionCenterInfo


def test_process_event() -> None:
    test_event = {
        "cc_info": {
            "rooms": "100"
        }
    }
    processor = CCInfoProcessor()

    assert processor.process_event(test_event) == ConventionCenterInfo(test_event["cc_info"])
