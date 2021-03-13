from .submit_cc_info import SubmitCCInfoController
from ...models import AuthContext, User, ConventionCenterInfo
from ...db import InMemoryDBInterface


def test_execute_pass() -> None:
    user_db = InMemoryDBInterface()

    username = "vale"
    auth_context = AuthContext(username)
    cc_info = ConventionCenterInfo({
        "sq_footage": "1000",
        "num_rooms": "5"
    })

    controller = SubmitCCInfoController(user_db, cc_info, auth_context)
    controller.execute()

    loaded_user = User.deserialize(user_db.get(username))

    assert cc_info.data == loaded_user.cc_info
