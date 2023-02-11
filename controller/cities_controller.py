from flask import Blueprint, Response, request

from controller.method import Method
from model import MapVisualizer
from service import CityService

blueprint = Blueprint('cities', __name__, url_prefix='/cities')

city_service = CityService()


@blueprint.route('/<int:city_id>/map', methods=[Method.GET])
def map_(city_id: int):
    city = city_service.get_by_id(city_id)
    map_visualizer = MapVisualizer(city)

    with_roads = request.args.get('roads', 'true') != 'false'
    with_places = request.args.get('places', 'true') != 'false'

    image = map_visualizer.print(with_roads, with_places)

    return Response(image.getvalue(), mimetype='image/png')
