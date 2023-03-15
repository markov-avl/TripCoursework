from flask import Blueprint, request
from werkzeug.exceptions import HTTPException

from entity import City
from service import CoordinateService, ImageService, PlaceService, CityService

from .form import PlaceForm
from .method import Method
from .helper import get_form, flash_message, flash_warning, flash_form_errors, ok, created, no_content, bad_request, \
    unprocessable_content

blueprint = Blueprint('places', __name__, url_prefix='/places')

coordinate_service = CoordinateService()
city_service = CityService()
place_service = PlaceService()
image_service = ImageService()


@blueprint.route('/', methods=[Method.GET])
def _get():
    city_id = _parse_integer_param('city_id')
    places = place_service.get_by_city(city_id) if city_id else place_service.get_all()
    data = [dict(id=p.id, name=p.name, address=p.address) for p in sorted(places, key=lambda p: p.name)]
    return ok(data=data)


@blueprint.route('/', methods=[Method.POST])
def _create():
    form: PlaceForm = get_form(PlaceForm)

    if form.validate_on_submit():
        try:
            coordinate = coordinate_service.create(form.city_id.data, form.longitude.data, form.latitude.data)
            place = place_service.create(coordinate, form.name.data, form.address.data)
            flash_message(f'Место успешно создано ({place.id})')
            _delete_images(place.coordinate.city)
            return created(id=place.id)
        except HTTPException as e:
            flash_warning(e.description)
            return unprocessable_content(errors=[e.description])

    flash_form_errors(form)
    return bad_request(errors=form.extended_errors)


@blueprint.route('/<int:place_id>', methods=[Method.PUT])
def _update(place_id: int):
    form: PlaceForm = get_form(PlaceForm)

    if form.validate_on_submit():
        try:
            place = place_service.get_by_id(place_id)
            city = place.coordinate.city
            coordinate_service.update(place.coordinate, form.city_id.data, form.longitude.data, form.latitude.data)
            place_service.update(place, name=form.name.data, address=form.address.data)
            flash_message(f'Место успешно изменено ({place.id})')
            _delete_images(*{city, place.coordinate.city})
            return no_content()
        except HTTPException as e:
            flash_warning(e.description)
            return unprocessable_content(errors=[e.description])

    flash_form_errors(form)
    return bad_request(errors=form.extended_errors)


@blueprint.route('/<int:place_id>', methods=[Method.DELETE])
def _delete(place_id: int):
    try:
        place = place_service.get_by_id(place_id)
        place_service.delete(place)
        flash_message(f'Место успешно удалено ({place.id})')
        _delete_images(place.coordinate.city)
        return no_content()
    except HTTPException as e:
        flash_warning(e.description)
        return unprocessable_content(errors=[e.description])


def _parse_integer_param(name: str) -> int | None:
    try:
        return int(request.args.get(name, ''))
    except ValueError:
        return


def _delete_images(*cities: City) -> None:
    for city in cities:
        image_service.delete_city_places(city)
