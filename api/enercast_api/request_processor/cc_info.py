from .abstract import AbstractProcessor
from ..models import ConventionCenterInfo


class CCInfoProcessor(AbstractProcessor):

    INFO_KEY = "cc_info"

    def process_event(self, event: dict) -> ConventionCenterInfo:
        return ConventionCenterInfo(event[CCInfoProcessor.INFO_KEY])
