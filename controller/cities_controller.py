from flask import Blueprint, Response, request, abort, render_template

from controller.method import Method
from model import MapVisualizer, ShortestPathFinder
from service import CityService, PlaceService, RoadService, ImageService

blueprint = Blueprint('cities', __name__, url_prefix='/cities')

city_service = CityService()
place_service = PlaceService()
road_service = RoadService()
image_service = ImageService()


@blueprint.route('/<int:city_id>/map', methods=[Method.GET])
def _map(city_id: int):
    city = city_service.get_by_id(city_id)
    map_visualizer = MapVisualizer(city)

    with_roads = _parse_boolean_param('roads')
    with_places = _parse_boolean_param('places')
    with_ids = _parse_boolean_param('ids')

    image = map_visualizer.print_map(with_roads, with_places, with_ids)

    return Response(image.getvalue(), mimetype='image/png')


@blueprint.route('/<int:city_id>/roads', methods=[Method.GET])
def _roads(city_id: int):
    city = city_service.get_by_id(city_id)
    roads = road_service.get_by_city(city)

    return render_template(
        'roads_input.jinja2',
        city=city,
        roads=roads,
        map_path=image_service.get_city_roads(city)
    )


@blueprint.route('/<int:city_id>/places', methods=[Method.GET])
def _places(city_id: int):
    city = city_service.get_by_id(city_id)
    places = place_service.get_by_city(city)

    return render_template(
        'city_places.jinja2',
        city=city,
        places=places,
        map_path=image_service.get_city_places(city)
    )


@blueprint.route('/<int:city_id>/shortest-path', methods=[Method.GET])
def _shortest_path(city_id: int):
    city = city_service.get_by_id(city_id)

    shortest_path_finder = ShortestPathFinder(city)
    map_visualizer = MapVisualizer(city)

    start_id = _parse_integer_param('start_id')
    destination_id = _parse_integer_param('destination_id')
    start = place_service.get_by_id(start_id)
    destination = place_service.get_by_id(destination_id)

    shortest_path = shortest_path_finder.find(start, destination)
    image = map_visualizer.print_shortest_path(shortest_path)

    return Response(image.getvalue(), mimetype='image/png')


def _parse_integer_param(name: str) -> int:
    try:
        return int(request.args.get(name, ''))
    except ValueError:
        abort(400, f'Параметр {name} не введен или не является целым числом')


def _parse_boolean_param(name: str) -> bool:
    return request.args.get(name, 'true') != 'false'
