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

    with_roads = request.args.get('roads', 'true') != 'false'
    with_places = request.args.get('places', 'true') != 'false'
    with_ids = request.args.get('ids', 'true') != 'false'

    image = map_visualizer.print(with_roads, with_places, with_ids)

    return Response(image.getvalue(), mimetype='image/png')


@blueprint.route('/<int:city_id>/roads', methods=[Method.GET])
def _roads(city_id: int):
    city = city_service.get_by_id(city_id)
    roads = road_service.get_by_city(city)

    return render_template(
        'template.jinja2',
        city=city,
        roads=roads,
        map_path=image_service.get_city_roads(city)
    )


@blueprint.route('/<int:city_id>/nearest-roads', methods=[Method.GET])
def _nearest_roads(city_id: int):
    city = city_service.get_by_id(city_id)
    map_visualizer = MapVisualizer(city)
    shortest_path_finder = ShortestPathFinder()

    with_ids = request.args.get('ids', 'true') != 'false'
    place_id = request.args.get('place_id', '')
    try:
        place_id = int(place_id)
    except ValueError:
        abort(400, 'place_id не введен или не является целым числом')

    place = place_service.get_by_id(place_id)

    nearest_roads = shortest_path_finder.find_nearest_roads(place)
    image = map_visualizer.print_nearest_roads(place, nearest_roads, with_ids)

    return Response(image.getvalue(), mimetype='image/png')


@blueprint.route('/<int:city_id>/shortest-path', methods=[Method.GET])
def _test(city_id: int):
    shortest_path_finder = ShortestPathFinder()

    city = city_service.get_by_id(city_id)
    roads = road_service.get_by_city(city)

    start_id = request.args.get('start_id', '')
    try:
        start_id = int(start_id)
    except ValueError:
        abort(400, 'start_id не введен или не является целым числом')

    destination_id = request.args.get('destination_id', '')
    try:
        destination_id = int(destination_id)
    except ValueError:
        abort(400, 'destination_id не введен или не является целым числом')

    start = place_service.get_by_id(start_id)
    destination = place_service.get_by_id(destination_id)

    shortest_path = shortest_path_finder.find(start, destination, roads)

    return '<br>'.join([
        f'Footpath distance: {shortest_path.footpath_distance}',
        f'Highway distance: {shortest_path.highway_distance}',
        f'Distance: {shortest_path.distance}',
        f'Straight distance: {shortest_path.straight_distance}',
        f'Points: {", ".join(map(lambda p: str(p.point), shortest_path.points))}'
    ])
