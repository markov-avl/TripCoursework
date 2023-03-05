from pathlib import Path

from flask import url_for

from entity import City
from model import MapVisualizer
from basedir import basedir


class ImageService:
    _CITY_ROADS = f'city-%d-roads.png'
    _CITY_PLACES = f'city-%d-places.png'

    def __init__(self):
        self._folder = Path(basedir).joinpath('static').joinpath('image')
        if not self._folder.exists():
            self._folder.mkdir(parents=True)

    def get_city_roads(self, city: City) -> str:
        image_name = self._CITY_ROADS % city.id
        if not self._folder.joinpath(image_name).exists():
            self.render_city_roads(city)
        return url_for('static', filename=f'image/{image_name}')

    def render_city_roads(self, city: City) -> None:
        map_visulizer = MapVisualizer(city)
        image = map_visulizer.print_city_roads()
        self._folder.joinpath(self._CITY_ROADS % city.id).write_bytes(image.getbuffer().tobytes())

    def get_city_places(self, city: City) -> str:
        image_name = self._CITY_PLACES % city.id
        if not self._folder.joinpath(image_name).exists():
            self.render_city_places(city)
        return url_for('static', filename=f'image/{image_name}')

    def render_city_places(self, city: City) -> None:
        map_visulizer = MapVisualizer(city)
        image = map_visulizer.print_city_places()
        self._folder.joinpath(self._CITY_PLACES % city.id).write_bytes(image.getbuffer().tobytes())
