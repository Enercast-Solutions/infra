from .contact_us import ContactUsController
from ...models import AuthContext, ContactUsFormData
from ...db import InMemoryDBInterface


def test_execute_pass() -> None:
    contact_us_db = InMemoryDBInterface()

    username = "vale"
    subject = "test subject"
    message = "test message"

    auth_context = AuthContext(username)
    form_data = ContactUsFormData(subject, message)

    output = ContactUsController(contact_us_db, auth_context, form_data).execute()

    correct_data = {
        "ID": output["ID"],
        "time_submitted": output["time_submitted"],
        "user_id": username,
        "subject": subject,
        "message": message
    }

    assert correct_data == contact_us_db.get(output["ID"])
