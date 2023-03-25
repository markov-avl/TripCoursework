from wtforms import IntegerField, DateField, BooleanField, TimeField
from wtforms.validators import InputRequired, Optional

from .form import Form


class VisitForm(Form):
    place_id = IntegerField(
        label='Место',
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
        ],
        format=['%Y-%m-%d', '%d.%m.%Y']
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
