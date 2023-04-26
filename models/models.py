from app import db, manager
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Post(db.Model):
    __tablename__ = "posts"
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
