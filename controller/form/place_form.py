from wtforms import StringField
from wtforms.validators import InputRequired

from .coordinate_form import CoordinateForm


class PlaceForm(CoordinateForm):
    name = StringField(
        label='Название',
        validators=[
            InputRequired(message='Обязательное поле')
        ]
    )
    address = StringField(
        label='Адрес',
        validators=[
            InputRequired(message='Обязательное поле')
        ]
    )
