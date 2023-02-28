from flask_sqlalchemy import SQLAlchemy

from basedir import basedir
from entity import Entity

database_name = 'trip.sqlite'
database_url = f'sqlite:///{basedir.joinpath(database_name)}'
database = SQLAlchemy(model_class=Entity)
