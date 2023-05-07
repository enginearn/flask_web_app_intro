from datetime import datetime

from flask_login import UserMixin
from apps.app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String, index=True, unique=True)
    # login = db.Column(db.Boolean(1), index=True, default=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.now, onupdate=datetime.now)

    def __repr__(self) -> str:
        return f'<User {self.id}>'

    @property
    def password(self) -> None:
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def is_duplicate(self, username: str, email: str) -> bool:
        return User.query.filter(
            (User.username == username) | (User.email == email)
        ).first() is not None

@login_manager.user_loader
def load_user(user_id: int) -> User:
    return User.query.get(int(user_id))
