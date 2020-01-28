from uuid import uuid4
from .base_otc import BaseOtc


class TripLinkOtc(BaseOtc):
    def __init__(self):
        super().__init__('trip_link')

    def create_otc(self):
        self._code = str(uuid4())
