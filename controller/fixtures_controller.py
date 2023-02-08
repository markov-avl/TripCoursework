from flask import Blueprint, current_app

from controller.method import Method
from database import database
from service import CityService, RoadService, CoordinateService, PlaceService

blueprint = Blueprint('fixtures', __name__, url_prefix='/fixtures')

city_service = CityService()
coordinate_service = CoordinateService()
road_service = RoadService()
place_service = PlaceService()


@blueprint.route('/load', methods=[Method.GET])
def load():
    recreate_schema()

    # Города
    vladivostok = city_service.create('Владивосток')

    # Координаты дорог
    road_coordinate_00 = coordinate_service.create(43.11630, 131.88244)
    road_coordinate_01 = coordinate_service.create(43.11573, 131.88549)
    road_coordinate_02 = coordinate_service.create(43.11527, 131.88826)
    road_coordinate_03 = coordinate_service.create(43.11804, 131.88631)
    road_coordinate_04 = coordinate_service.create(43.11862, 131.88327)

    # Координаты мест
    place_coordinate_00 = coordinate_service.create(43.11662, 131.88268)
    place_coordinate_01 = coordinate_service.create(43.11673, 131.88562)

    # Дороги
    road_service.create(vladivostok, road_coordinate_00, road_coordinate_01)
    road_service.create(vladivostok, road_coordinate_01, road_coordinate_02)
    road_service.create(vladivostok, road_coordinate_01, road_coordinate_03)
    road_service.create(vladivostok, road_coordinate_03, road_coordinate_04)
    road_service.create(vladivostok, road_coordinate_00, road_coordinate_04)

    # Места
    place_service.create(vladivostok, place_coordinate_00, 'Шоколадница', 'Алеутская улица, 20')
    place_service.create(vladivostok, place_coordinate_01, 'Лима', 'Океанский проспект, 7')

    return 'Loaded!'


def recreate_schema() -> None:
    with current_app.app_context():
        database.drop_all()
        database.create_all()
