__author__ = 'at'

from app import db
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    age = db.Column(db.String())
    result = db.Column(JSON)

    def __init__(self, _id, name, age, result):
        self.id = _id
        self.name = name
        self.age = age
        self.result = result

    def __repr__(self):
        return '<id {}>'.format(self.id)