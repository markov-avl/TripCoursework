from wtforms import IntegerField
from wtforms.validators import InputRequired

from .validator import DiffersFrom
from .form import Form


class RoadForm(Form):
    point_0_id = IntegerField(
        label='ID одного конца дороги',
        validators=[
            InputRequired(message='Обязательное поле')
        ]
    )
    point_1_id = IntegerField(
        label='ID второго конца дороги',
        validators=[
            InputRequired(message='Обязательное поле'),
            DiffersFrom(fieldname='point_0_id', message='ID концов дорог должны отличаться')
        ]
    )
