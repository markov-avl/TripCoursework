from flask import Blueprint, request, flash

from .coordinate_form import CoordinateForm
from controller.method import Method
from service import CityService, CoordinateService

from werkzeug.exceptions import HTTPException

from .helper import redirect

blueprint = Blueprint('coordinates', __name__, url_prefix='/coordinates')

city_service = CityService()
coordinate_service = CoordinateService()


@blueprint.route('/', methods=[Method.POST])
def _create():
    form = CoordinateForm(request.form) if request.form else CoordinateForm(data=request.json)

    if form.validate_on_submit():
        try:
            city = city_service.get_by_id(form.city_id.data)
            coordinate = coordinate_service.create(city, form.longitude.data, form.latitude.data)
            flash(f'Координата успешно создана ({coordinate.id})')
        except HTTPException as e:
            flash(e.description, 'warning')
    else:
        for field, messages in form.errors.items():
            message = '; '.join(m.lower() for m in messages)
            flash(f'{getattr(form, field).label.text}: {message}.', 'warning')

    return redirect()
