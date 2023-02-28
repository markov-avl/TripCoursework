from flask import Blueprint
from werkzeug.exceptions import HTTPException

from controller.method import Method
from service import CityService, CoordinateService

from .form import CoordinateForm
from .helper import redirect, get_form, flash_message, flash_warning, flash_form_errors

blueprint = Blueprint('coordinates', __name__, url_prefix='/coordinates')

city_service = CityService()
coordinate_service = CoordinateService()


@blueprint.route('/', methods=[Method.POST])
def _create():
    form: CoordinateForm = get_form(CoordinateForm)

    if form.validate_on_submit():
        try:
            city = city_service.get_by_id(form.city_id.data)
            coordinate = coordinate_service.create(city, form.longitude.data, form.latitude.data)
            flash_message(f'Координата успешно создана ({coordinate.id})')
        except HTTPException as e:
            flash_warning(e.description)
    else:
        flash_form_errors(form)

    return redirect()
