from flask import Blueprint, redirect, url_for

from .method import Method
from service import TripService

blueprint = Blueprint('index', __name__)

trip_service = TripService()


@blueprint.route('/', methods=[Method.GET])
def _index():
    trip = trip_service.create()
    return redirect(url_for('trip._index', secret=trip.secret))
