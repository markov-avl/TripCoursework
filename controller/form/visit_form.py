from wtforms import IntegerField, DateField, BooleanField, TimeField
from wtforms.validators import InputRequired, Optional

from .form import Form


class VisitForm(Form):
    place_id = IntegerField(
        label='ID места',
        validators=[
            InputRequired(message='Обязательное поле')
        ]
    )
    stay_time = TimeField(
        label='Длительность',
        validators=[
            InputRequired(message='Обязательное поле')
        ]
    )
    date = DateField(
        label='Дата',
        validators=[
            Optional()
        ]
    )
    time = TimeField(
        label='Время',
        validators=[
            Optional()
        ]
    )
    priority = BooleanField(
        label='Обязательно',
        default=True
    )
