from pathlib import Path

from flask import Flask

import controller

from service import db

basedir = Path(__file__).parent

app = Flask(__name__)
app.register_blueprint(controller.index_blueprint)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(basedir.joinpath('trip.sqlite'))

db.init_app(app)

if __name__ == '__main__':
    with app.app_context() as context:
        db.create_all()
    app.run(debug=True)
