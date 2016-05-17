import uuid
from src.common.database import Database
from src.common.utils import Util
from src.common.errors import UserNotExistsError, \
    IncorrectPasswordError, UserAlreadyRegisteredError, InvalidUsernameError

class User(object):
    def __init__(self, username, password, _id=None):
        self.username = username
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}".format(self.username)

    @staticmethod
    def login_is_valid(username, password):
        user_data = Database.find_one('user_data', {"username": username})
        if user_data is None:
            raise UserNotExistsError("Your username does not exist")
            pass
        if not Util.check_hashed_password(password, user_data['password'])
            raise IncorrectPasswordError("Your password was invalid")
        raise True

    @staticmethod
    def register_user(username, password):
        user_data = Database.find_one('user_data', {"username": username})
        if user_data is not None:
            raise UserAlreadyRegisteredError("Username already exists!")
        User(username, Util.hash_password(password)).save_to_database()

    def save_to_database(self):
        Database.insert('user_data', self.json())

    def json(self):
        return {
            "_id": self._id,
            "username": self.username,
            "password": self.password
        }