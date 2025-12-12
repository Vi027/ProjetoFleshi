from flask_login import UserMixin
from appfleshi import database, login_manager
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(20), unique=True, nullable=False)
    email = database.Column(database.String(100), unique=True, nullable=False)
    password = database.Column(database.String(60), nullable=False)
    photos =  database.relationship('Photo', backref='user', lazy=True)


class Photo(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    filename = database.Column(database.String(255), default="default.png")
    upload_date = database.Column(database.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)

    comments = database.relationship('Comment', backref='photo', lazy=True)
    likes = database.relationship('Like', backref='photo', lazy=True)


class Like(database.Model):
    __tablename__ = 'like'
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))
    photo_id = database.Column(database.Integer, database.ForeignKey('photo.id'))

class Comment(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    content = database.Column(database.String(300), nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    photo_id = database.Column(database.Integer, database.ForeignKey('photo.id'), nullable=False)
    timestamp = database.Column(database.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    user = database.relationship('User', backref='comments')


