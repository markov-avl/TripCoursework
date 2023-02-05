from flask import Blueprint

from controller.method import Method

blueprint = Blueprint('index', __name__)


@blueprint.route('/', methods=[Method.GET])
def index():
    return 'Hello!'
