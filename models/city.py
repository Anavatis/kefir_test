from app import db


class City(db.Model):
    __tablename__ = 'city'

    id_ = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    city_name = db.Column(db.String(100), nullable=False)

    users = db.relationship('User', backref="city")