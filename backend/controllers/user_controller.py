from models.users_model import User
from extensions import db


def create_user(data):
    try:
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        raise e
