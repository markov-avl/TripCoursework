from flask import Blueprint, Response, request, abort, render_template

from controller.method import Method
from model import MapVisualizer, NearestRoadSearcher
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
    nearest_road_searcher = NearestRoadSearcher()

    with_ids = request.args.get('ids', 'true') != 'false'
    place_id = request.args.get('place_id', '')
    try:
        place_id = int(place_id)
    except ValueError:
        abort(400, 'place_id не введен или не является целым числом')

    place = place_service.get_by_id(place_id)

    nearest_roads = nearest_road_searcher.find(place)
    image = map_visualizer.print_nearest_roads(place, nearest_roads, with_ids)

    return Response(image.getvalue(), mimetype='image/png')
