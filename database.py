from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, Engine

from basedir import basedir
from entity import Entity

database_name = 'trip.sqlite'
database_url = f'sqlite:///{basedir.joinpath(database_name)}'
database = SQLAlchemy(model_class=Entity)


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, _):
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')
    cursor.close()
