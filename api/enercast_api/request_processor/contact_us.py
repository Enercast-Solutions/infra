from .abstract import AbstractProcessor
from ..models import ContactUsFormData


class ContactUsProcessor(AbstractProcessor):

    def process_event(self, event: dict) -> ContactUsFormData:
        return ContactUsFormData(event["subject"], event["message"])
