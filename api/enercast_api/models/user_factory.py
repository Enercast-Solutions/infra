from .user import User


class UserFactory:

    @staticmethod
    def create_default_user(id: str) -> User:
        cc_info = dict()
        energy_consumption_predictions = list()

        return User(id,
                    cc_info,
                    energy_consumption_predictions)
