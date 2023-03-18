from flask import Blueprint, render_template

from .method import Method
from service import TripService

blueprint = Blueprint('trip', __name__, url_prefix='/trips')

trip_service = TripService()


@blueprint.route('/<string:secret>', methods=[Method.GET])
def _index(secret: str):
    trip = trip_service.get_by_secret(secret)

    # return render_template(
    #     'data_redactor.jinja2',
    #     trip=trip
    # )
    return f'Trip ID: {trip.id}<br>Trip secret: {trip.secret}'
