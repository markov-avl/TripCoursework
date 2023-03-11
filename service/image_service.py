from io import BytesIO
from pathlib import Path

from flask import url_for

from entity import City
from model import MapVisualizer
from basedir import basedir


class ImageService:
    _CITY_ROADS = f'city-%d-roads.png'
    _CITY_PLACES = f'city-%d-places.png'
    _CONTROLLER = 'static'
    _IMAGE_FOLDER = 'image'

    def __init__(self):
        self._folder = Path(basedir).joinpath(self._CONTROLLER).joinpath(self._IMAGE_FOLDER)
        if not self._folder.exists():
            self._folder.mkdir(parents=True)

    def get_city_roads(self, city: City) -> str:
        image_name = self._CITY_ROADS % city.id
        if not self._folder.joinpath(image_name).exists():
            map_visulizer = MapVisualizer(city)
            image = map_visulizer.print_city_roads()
            self._save_image(image_name, image)
        return self._image_url(image_name)

    def delete_city_roads(self, city: City) -> None:
        self._delete_image(self._CITY_ROADS % city.id)

    def get_city_places(self, city: City) -> str:
        image_name = self._CITY_PLACES % city.id
        if not self._folder.joinpath(image_name).exists():
            map_visulizer = MapVisualizer(city)
            image = map_visulizer.print_city_places()
            self._save_image(image_name, image)
        return self._image_url(image_name)

    def delete_city_places(self, city: City) -> None:
        self._delete_image(self._CITY_PLACES % city.id)

    def _save_image(self, image_name: str, image: BytesIO) -> None:
        self._folder.joinpath(image_name).write_bytes(image.getbuffer().tobytes())

    def _delete_image(self, image_name: str) -> None:
        self._folder.joinpath(image_name).unlink(missing_ok=True)

    def _image_url(self, image_name: str) -> str:
        return url_for(self._CONTROLLER, filename=f'{self._IMAGE_FOLDER}/{image_name}')
