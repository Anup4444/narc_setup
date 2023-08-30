# setup/dbsetup.py

from flask_sqlalchemy import SQLAlchemy

DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/narc_setup'

db = SQLAlchemy()


def create_tables(app):
    with app.app_context():
        db.create_all()
