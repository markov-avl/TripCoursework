import os

from flask import Flask

import controller
from database import database, database_url

app = Flask(__name__)
app.secret_key = os.urandom(32)

# Регистрация эндпоинтов
app.register_blueprint(controller.index_blueprint)
app.register_blueprint(controller.fixtures_blueprint)
app.register_blueprint(controller.cities_blueprint)
app.register_blueprint(controller.coordinates_blueprint)
app.register_blueprint(controller.roads_blueprint)
app.register_blueprint(controller.places_blueprint)

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
database.init_app(app)

# Расширение глобальных переменных/функций шаблонизатора
app.jinja_env.globals['enumerate'] = enumerate
app.jinja_env.globals['range'] = range

if __name__ == '__main__':
    app.run(debug=True)
