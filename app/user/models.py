from app import db
from app.extensions import pwd_context


class City(db.Model):
    __tablename__ = 'city'

    id_ = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    city_name = db.Column(db.String(100), nullable=False)

    users = db.relationship('User', backref="city")


class User(db.Model):
    __tablename__ = 'user'

    id_ = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    cookie_token = db.Column(db.String(150), default="")
    login = db.Column(db.String(100))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    other_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    city_id = db.Column(db.Integer(), db.ForeignKey(City.id_))
    phone = db.Column(db.Integer())
    birthday = db.Column(db.Date)
    additional_info = db.Column(db.Text())
    is_admin = db.Column(db.Boolean(), default=False)
    _password = db.Column("password", db.String(255), nullable=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def check_password(self, password) -> bool:
        return pwd_context.hash(password) == self.password

    def get_private_data(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "other_name": self.other_name,
            "email": self.email,
            "phone": self.phone,
            "birthday": self.birthday,
            "is_admin": self.is_admin
        }

    def get_public_data(self):
        return {
            "id": self.id_,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }