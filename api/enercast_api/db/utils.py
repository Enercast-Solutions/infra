from .db import DB
from ..models import User, UserFactory


def load_user(db: DB, id: str) -> User:
    try:
        return User.deserialize(db.get(id))
    except:
        return UserFactory.create_default_user(id)
