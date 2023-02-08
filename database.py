from flask_sqlalchemy import SQLAlchemy

from entity import Entity

database = SQLAlchemy(model_class=Entity)
