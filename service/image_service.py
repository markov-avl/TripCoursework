from pathlib import Path

from flask import url_for

from entity import City
from model import MapVisualizer
from basedir import basedir


class ImageService:
    def __init__(self):
        self._folder = Path(basedir).joinpath('static').joinpath('image')
        if not self._folder.exists():
            self._folder.mkdir(parents=True)

    def get_city_roads(self, city: City) -> str:
        image_name = f'city-{city.id}-roads.png'
        if not self._folder.joinpath(image_name).exists():
            map_visulizer = MapVisualizer(city)
            image = map_visulizer.print_map(with_roads=True, with_places=False, with_ids=True)
            self._folder.joinpath(image_name).write_bytes(image.getbuffer().tobytes())
        return url_for('static', filename=f'image/{image_name}')
