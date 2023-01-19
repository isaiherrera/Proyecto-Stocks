from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from flask import current_app, g
import sqlite3

engine = create_engine('sqlite:///instance/almacen.db',
                       connect_args={'check_same_thread': False})

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
