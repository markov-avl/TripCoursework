from wtforms import StringField
from wtforms.validators import InputRequired

from .form import Form


class CityForm(Form):
    name = StringField(
        label='Название',
        validators=[
            InputRequired(message='Обязательное поле')
        ]
    )
