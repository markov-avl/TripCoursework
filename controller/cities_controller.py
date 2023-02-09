from flask import Blueprint, Response

from controller.method import Method
from model import MapVisualizer
from service import CityService, RoadService, PlaceService

blueprint = Blueprint('cities', __name__, url_prefix='/cities')

city_service = CityService()
road_service = RoadService()
place_service = PlaceService()


@blueprint.route('/<int:city_id>/map', methods=[Method.GET])
def map_(city_id: int):
    city = city_service.get_by_id(city_id)
    roads = road_service.get_by_city(city)
    places = place_service.get_by_city(city)

    image = MapVisualizer.print(roads, places)

    return Response(image.getvalue(), mimetype='image/png')
