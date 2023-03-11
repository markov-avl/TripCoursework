from flask import Blueprint
from werkzeug.exceptions import HTTPException

from controller.method import Method
from entity import City
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
            _delete_images(*{road.point_0.city, road.point_1.city})
        except HTTPException as e:
            flash_warning(e.description)
    else:
        flash_form_errors(form)

    return redirect()


@blueprint.route('/<int:road_id>', methods=[Method.PUT])
def _update(road_id: int):
    form: RoadForm = get_form(RoadForm)

    if form.validate_on_submit():
        try:
            road = road_service.get_by_id(road_id)
            road.point_0 = coordinate_service.get_by_id(form.point_0_id.data)
            road.point_1 = coordinate_service.get_by_id(form.point_1_id.data)
            road_service.update(road)
            flash_message(f'Дорога успешно изменена ({road.id})')
            _delete_images(*{road.point_0.city, road.point_1.city})
        except HTTPException as e:
            flash_warning(e.description)
    else:
        flash_form_errors(form)

    return redirect()


@blueprint.route('/<int:road_id>', methods=[Method.DELETE])
def _delete(road_id: int):
    try:
        road = road_service.get_by_id(road_id)
        road_service.delete(road)
        flash_message(f'Дорога успешно удалена ({road.id})')
        _delete_images(*{road.point_0.city, road.point_1.city})
    except HTTPException as e:
        flash_warning(e.description)

    return redirect()


def _delete_images(*cities: City) -> None:
    for city in cities:
        image_service.delete_city_roads(city)
        image_service.delete_city_places(city)
