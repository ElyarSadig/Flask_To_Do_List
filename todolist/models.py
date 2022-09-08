from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    description = db.Column(db.String(1000))
    complete = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return self.title


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    tasks = db.relationship('Task', lazy=True, backref='tasks')







