from werkzeug.security import check_password_hash, generate_password_hash

from App.ext import db
from App.models import BaseModel

PERMISSION_NONE = 0
PERMISSION_COMMON = 2


class AdminUser(BaseModel):

    username = db.Column(db.String(32), unique=True)
    _password = db.Column(db.String(256))
    is_delete = db.Column(db.Boolean, default=False)
    is_super = db.Column(db.Boolean, default=False)
    permission = db.Column(db.Boolean, default=PERMISSION_NONE)

    @property
    def password(self):
        raise Exception("can't access")

    @password.setter
    def password(self, password_value):
        self._password = generate_password_hash(password_value)

    def check_password(self, password_value):
        return check_password_hash(self._password, password_value)

    def check_permission(self, permission):
        return self.is_super or permission & self.permission == permission