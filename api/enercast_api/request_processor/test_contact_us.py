from .contact_us import ContactUsProcessor
from ..models import ContactUsFormData


def test_process_event() -> None:
    test_event = {
        "subject": "woo subject",
        "message": "woo message"
    }
    processor = ContactUsProcessor()

    assert processor.process_event(test_event) == ContactUsFormData(test_event["subject"], test_event["message"])
