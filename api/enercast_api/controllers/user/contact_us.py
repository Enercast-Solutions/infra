from ..abstract import AbstractController
from ...db import DB
from time import time
from ...utils import generate_id
from ...models import AuthContext, ContactUsFormData, ContactUs


class ContactUsController(AbstractController):

    def __init__(self,
                 contact_us_db: DB,
                 auth_context: AuthContext,
                 data: ContactUsFormData):
        self._contact_us_db = contact_us_db
        self._auth_context = auth_context
        self._data = data

    def execute(self) -> dict:
        contact_us = ContactUs(generate_id(),
                               str(time()),
                               self._auth_context.id,
                               self._data.subject,
                               self._data.message)

        self._contact_us_db.create_or_update(contact_us.id, contact_us.serialize())

        return contact_us.serialize()
