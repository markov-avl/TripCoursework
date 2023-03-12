from flask import Blueprint, Response, request, abort, render_template
from werkzeug.exceptions import HTTPException

from entity import City
from model import MapVisualizer, ShortestPathFinder
from service import CityService, PlaceService, RoadService, ImageService

from .form import CityForm
from .method import Method
from .helper import get_form, flash_message, flash_warning, flash_form_errors, created, no_content, bad_request, \
    unprocessable_content

blueprint = Blueprint('cities', __name__, url_prefix='/cities')

city_service = CityService()
place_service = PlaceService()
road_service = RoadService()
image_service = ImageService()


@blueprint.route('/', methods=[Method.GET])
def _index():
    cities = sorted(city_service.get_all(), key=lambda c: c.name)

    return render_template(
        'cities.jinja2',
        cities=cities
    )


@blueprint.route('/', methods=[Method.POST])
def _create():
    form: CityForm = get_form(CityForm)

    if form.validate_on_submit():
        try:
            city = city_service.create(form.name.data)
            flash_message(f'Город успешно создан ({city.id})')
            return created(id=city.id)
        except HTTPException as e:
            flash_warning(e.description)
            return unprocessable_content(errors=[e.description])

    flash_form_errors(form)
    return bad_request(errors=form.extended_errors)


@blueprint.route('/<int:city_id>', methods=[Method.PUT])
def _update(city_id: int):
    form: CityForm = get_form(CityForm)

    if form.validate_on_submit():
        try:
            city = city_service.update(city_id, form.name.data)
            flash_message(f'Город успешно изменен ({city.id})')
            return no_content()
        except HTTPException as e:
            flash_warning(e.description)
            return unprocessable_content(errors=[e.description])

    flash_form_errors(form)
    return bad_request(errors=form.extended_errors)


@blueprint.route('/<int:city_id>', methods=[Method.DELETE])
def _delete(city_id: int):
    try:
        city = city_service.get_by_id(city_id)
        city_service.delete(city)
        flash_message(f'Город успешно удален ({city.id})')
        _delete_images(city)
        return no_content()
    except HTTPException as e:
        flash_warning(e.description)
        return unprocessable_content(errors=[e.description])


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
    roads = sorted(road_service.get_by_city(city), key=lambda r: (r.point_0.id, r.point_1.id))

    return render_template(
        'city_roads.jinja2',
        city=city,
        roads=roads,
        map_path=image_service.get_city_roads(city)
    )


@blueprint.route('/<int:city_id>/places', methods=[Method.GET])
def _places(city_id: int):
    city = city_service.get_by_id(city_id)
    places = sorted(place_service.get_by_city(city), key=lambda p: p.coordinate.id)

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


def _delete_images(*cities: City) -> None:
    for city in cities:
        image_service.delete_city_roads(city)
        image_service.delete_city_places(city)
