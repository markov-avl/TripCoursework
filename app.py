from flask import Flask

import controller
from basedir import basedir
from database import database

app = Flask(__name__)

# Регистрация эндпоинтов
app.register_blueprint(controller.index_blueprint)
app.register_blueprint(controller.fixtures_blueprint)
app.register_blueprint(controller.cities_blueprint)

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(basedir.joinpath('trip.sqlite'))
database.init_app(app)

# Расширение глобальных переменных/функций шаблонизатора
app.jinja_env.globals['enumerate'] = enumerate
app.jinja_env.globals['range'] = range

if __name__ == '__main__':
    app.run(debug=True)
