from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, doc: dict | None):
        self._doc = doc or {}

    def get_id(self) -> str:
        _id = self._doc.get("_id")
        return str(_id) if _id else ""

    @property
    def name(self): return self._doc.get("name","")
    @property
    def email(self): return self._doc.get("email","")
    @property
    def role(self): return self._doc.get("role","user")
    @property
    def password_hash(self): return self._doc.get("password_hash","")
