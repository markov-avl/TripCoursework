from flask import Blueprint, render_template, redirect, url_for

from entity import Priority
from model import Router
from .form import TripForm
from .helper import get_form, flash_form_errors, ok, flash_errors
from .method import Method
from service import TripService, CityService, VisitService, PlaceService

blueprint = Blueprint('trips', __name__, url_prefix='/trips')

trip_service = TripService()
city_service = CityService()
visit_service = VisitService()
place_service = PlaceService()


@blueprint.route('/<string:secret>', methods=[Method.GET])
def _index(secret: str):
    # TODO: когда будет более или менее стабильная версия, вернуть эту строчку
    # trip = trip_service.get_by_secret(secret)
    trip = trip_service.get_by_id(int(secret)) if secret.isdigit() else trip_service.get_by_secret(secret)  # для дебага
    visits = sorted(visit_service.get_by_trip(trip), key=lambda v: v.id)
    cities = sorted(city_service.get_all(), key=lambda c: c.name)
    places = sorted(place_service.get_by_city(trip.city), key=lambda p: p.name) if trip.city else []

    return render_template(
        'data_editor.jinja2',
        trip=trip,
        visits=visits,
        cities=cities,
        places=places,
        Priority=Priority
    )


@blueprint.route('/<string:secret>', methods=[Method.PUT])
def _update(secret: str):
    form: TripForm = get_form(TripForm)
    form.validate()

    trip = trip_service.update(secret,
                               form.city_id.data,
                               form.accommodation_id.data,
                               form.starts_at.data,
                               form.ends_at.data if 'ends_at' not in form.errors else None,
                               form.awakens_at.data,
                               form.rests_at.data if 'rests_at' not in form.errors else None)

    visit_service.delete_by_trip(trip)
    for visit in form.visits.entries:
        visit_service.create(trip,
                             visit.form.place_id.data,
                             Priority.HIGH if visit.form.priority.data else Priority.LOW,
                             visit.form.stay_time.data,
                             visit.form.date.data,
                             visit.form.time.data)

    flash_form_errors(form)
    return ok(errors=form.extended_errors)


@blueprint.route('/<string:secret>/routes', methods=[Method.GET])
def _routes(secret: str):
    # TODO: когда будет более или менее стабильная версия, вернуть эту строчку
    # trip = trip_service.get_by_secret(secret)
    trip = trip_service.get_by_id(int(secret)) if secret.isdigit() else trip_service.get_by_secret(secret)  # для дебага

    route = Router(trip).get()
    if route.success:
        return '<br><br>'.join(f'Visit: {d.visit.place.name}<br>'
                               f'Datetime: {d.datetime}<br>'
                               f'Distance: {d.distance}<br>'
                               f'Time to get: {d.time_to_get}'
                               for d in route.data)

    flash_errors(route.errors)
    return redirect(url_for('trips._index', secret=trip.secret))
