from flask import Blueprint, render_template

from controller.method import Method
from service import CityService

blueprint = Blueprint('index', __name__)
city_service = CityService()


@blueprint.route('/', methods=[Method.GET])
def index():
    cities = sorted(city_service.get_all(), key=lambda c: c.name)

    return render_template(
        'data_editor.jinja2',
        cities=cities
    )

# @blueprint.route('/editor', methods=[Method.GET])
# def _index():
#     cities = sorted(city_service.get_all(), key=lambda c: c.name)
#
#     return render_template(
#         'data_editor.jinja2',
#         cities=cities
#     )
