from flask_sqlalchemy import SQLAlchemy

from entity import Entity

db = SQLAlchemy(model_class=Entity)
