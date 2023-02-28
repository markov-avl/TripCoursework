from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import InputRequired

from .validator import DiffersFrom


class RoadForm(FlaskForm):
    class Meta:
        csrf = False

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
