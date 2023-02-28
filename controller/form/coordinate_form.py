from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField
from wtforms.validators import InputRequired, NumberRange


class CoordinateForm(FlaskForm):
    class Meta:
        csrf = False

    city_id = IntegerField(
        label='ID города',
        validators=[
            InputRequired(message='Обязательное поле')
        ]
    )
    longitude = FloatField(
        label='Долгота',
        validators=[
            InputRequired(message='Обязательное поле'),
            NumberRange(min=-180.0, max=180.0, message='Долгота не может быть меньше -180 или больше 180 градусов')
        ]
    )
    latitude = FloatField(
        label='Широта',
        validators=[
            InputRequired(message='Обязательное поле'),
            NumberRange(min=-90.0, max=90.0, message='Широта не может быть меньше -90 или больше 90 градусов')
        ]
    )
