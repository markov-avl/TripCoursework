from io import BytesIO

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from flask import Blueprint, send_file, Response

from controller.method import Method
from service import CityService, RoadService, CoordinateService, PlaceService

blueprint = Blueprint('cities', __name__, url_prefix='/cities')

city_service = CityService()
coordinate_service = CoordinateService()
road_service = RoadService()
place_service = PlaceService()


@blueprint.route('/<int:id_>/map', methods=[Method.GET])
def map_(id_: int):
    city = city_service.get_by_id(id_)
    roads = road_service.get_by_city(city)
    places = place_service.get_by_city(city)

    fig, ax = plt.subplots(figsize=(12, 8), frameon=False)

    m = Basemap(projection='gnom', lat_0=roads[0].edge_0.latitude, lon_0=roads[0].edge_0.longitude,
                width=1200, height=800, resolution='i')

    x = [place.coordinate.longitude for place in places]
    y = [place.coordinate.latitude for place in places]
    m.scatter(x, y, latlon=True, marker='D', color='red', s=3)

    for place in places:
        x, y = m(place.coordinate.longitude, place.coordinate.latitude)
        plt.text(x + 15, y, place.name, fontsize=8,
                 ha='left', va='center', color='k', bbox=dict(facecolor='w', alpha=0.2))

    for road in roads:
        x = [road.edge_0.longitude, road.edge_1.longitude]
        y = [road.edge_0.latitude, road.edge_1.latitude]
        m.plot(x, y, latlon=True, marker=None, color='black')

    image = BytesIO()
    fig.savefig(image, dpi=400., format='png', bbox_inches='tight', pad_inches=0)

    return Response(image.getvalue(), mimetype='image/png')
