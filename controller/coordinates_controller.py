from flask import Blueprint
from werkzeug.exceptions import HTTPException

from controller.method import Method
from entity import City
from service import CityService, CoordinateService, ImageService

from .form import CoordinateForm
from .helper import get_form, flash_message, flash_warning, flash_form_errors, created, bad_request, \
    unprocessable_content

blueprint = Blueprint('coordinates', __name__, url_prefix='/coordinates')

city_service = CityService()
coordinate_service = CoordinateService()
image_service = ImageService()


@blueprint.route('/', methods=[Method.POST])
def _create():
    form: CoordinateForm = get_form(CoordinateForm)

    if form.validate_on_submit():
        try:
            coordinate = coordinate_service.create(form.city_id.data, form.longitude.data, form.latitude.data)
            flash_message(f'Координата успешно создана ({coordinate.id})')
            _delete_images(coordinate.city)
            return created(id=coordinate.id)
        except HTTPException as e:
            flash_warning(e.description)
            return unprocessable_content(errors=[e.description])

    flash_form_errors(form)
    return bad_request(errors=form.extended_errors)


def _delete_images(*cities: City) -> None:
    for city in cities:
        image_service.delete_city_roads(city)
