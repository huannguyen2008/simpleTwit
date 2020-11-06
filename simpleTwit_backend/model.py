from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


class User(db.Model, UserMixin, SerializerMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(30), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Tweet(db.Model, SerializerMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(280), nullable=False)
    tweet = Column(String(280), nullable=False)
    date = Column(DateTime, unique=True, nullable=False, default=datetime)

    def __repr__(self):
        return f"Tweet('{self.name}','{self.tweet}','{self.date}')"
