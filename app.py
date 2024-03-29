import os
from datetime import datetime

import wtforms_json
from flask import Flask

import controller
from database import database, database_url

app = Flask(__name__)
app.secret_key = os.urandom(32)
app.config['JSON_AS_ASCII'] = False

# Регистрация эндпоинтов
app.register_blueprint(controller.index_blueprint)
app.register_blueprint(controller.fixtures_blueprint)
app.register_blueprint(controller.cities_blueprint)
app.register_blueprint(controller.coordinates_blueprint)
app.register_blueprint(controller.roads_blueprint)
app.register_blueprint(controller.places_blueprint)
app.register_blueprint(controller.trip_blueprint)

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
database.init_app(app)

# Настройка форм
wtforms_json.init()

# Расширение глобальных переменных/функций шаблонизатора
app.jinja_env.globals['enumerate'] = enumerate
app.jinja_env.globals['range'] = range
app.jinja_env.globals['datetime'] = datetime

if __name__ == '__main__':
    app.run(debug=True)
