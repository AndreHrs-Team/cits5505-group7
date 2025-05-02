import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_db_uri = f"sqlite:///{os.path.join(basedir, 'app.db')}"


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI') or default_db_uri
    SECRET_KEY = os.getenv("SECRET_KEY")
    print(SQLALCHEMY_DATABASE_URI)
