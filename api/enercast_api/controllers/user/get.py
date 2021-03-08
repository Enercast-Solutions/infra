from ..abstract import AbstractController
from ...db import DB, load_user
from ...models import AuthContext


class GetUserController(AbstractController):

    def __init__(self,
                 user_db: DB,
                 auth_context: AuthContext):
        self._user_db = user_db
        self._auth_context = auth_context

    def execute(self) -> dict:
        user = load_user(self._user_db, self._auth_context.id)

        # Sure, we're making a 2nd call to the DB...but who cares?
        self._user_db.create_or_update(user.id, user.serialize())

        return user.serialize()
