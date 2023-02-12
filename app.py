from flask import Flask

import controller
from basedir import basedir
from database import database

app = Flask(__name__)
app.register_blueprint(controller.index_blueprint)
app.register_blueprint(controller.fixtures_blueprint)
app.register_blueprint(controller.cities_blueprint)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(basedir.joinpath('trip.sqlite'))

database.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
