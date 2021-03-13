from ..abstract import AbstractController
from ...db import DB, load_user
from ...models import AuthContext, ConventionCenterInfo


class SubmitCCInfoController(AbstractController):

    def __init__(self,
                 user_db: DB,
                 cc_info: ConventionCenterInfo,
                 auth_context: AuthContext):
        self._user_db = user_db
        self._cc_info = cc_info
        self._auth_context = auth_context

    def execute(self) -> None:
        user = load_user(self._user_db, self._auth_context.id)

        user.cc_info = self._cc_info.data

        self._user_db.create_or_update(user.id, user.serialize())
