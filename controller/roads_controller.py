from flask import Blueprint
from werkzeug.exceptions import HTTPException

from controller.method import Method
from service import CoordinateService, RoadService, ImageService

from .form import RoadForm
from .helper import redirect, get_form, flash_message, flash_warning, flash_form_errors

blueprint = Blueprint('roads', __name__, url_prefix='/roads')

coordinate_service = CoordinateService()
road_service = RoadService()
image_service = ImageService()


@blueprint.route('/', methods=[Method.POST])
def _create():
    form: RoadForm = get_form(RoadForm)

    if form.validate_on_submit():
        try:
            point_0 = coordinate_service.get_by_id(form.point_0_id.data)
            point_1 = coordinate_service.get_by_id(form.point_1_id.data)
            road = road_service.create(point_0, point_1)
            flash_message(f'Дорога успешно создана ({road.id})')
            for city in {point_0.city, point_1.city}:
                image_service.render_city_roads(city)
        except HTTPException as e:
            flash_warning(e.description)
    else:
        flash_form_errors(form)

    return redirect()
