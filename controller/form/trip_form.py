from wtforms import IntegerField, DateField, FieldList, FormField
from wtforms.validators import InputRequired

from .visit_form import VisitForm
from .validator import LaterThanOrAt, MinimalLength

from .form import Form


class TripForm(Form):
    city_id = IntegerField(
        label='ID города',
        validators=[
            InputRequired(message='Обязательное поле')
        ]
    )
    accommodation_id = IntegerField(
        label='ID ночлега',
        validators=[
            InputRequired(message='Обязательное поле')
        ]
    )
    starts_at = DateField(
        label='Дата начала путешествия',
        validators=[
            InputRequired(message='Обязательное поле')
        ]
    )
    ends_at = DateField(
        label='Дата окончания путешествия',
        validators=[
            InputRequired(message='Обязательное поле'),
            LaterThanOrAt(message='Дата окончания путешествия должна быть позже или равна '
                                  'дате начала',
                          fieldname='starts_at')
        ]
    )
    awakens_at = DateField(
        label='Время начала периода бодрствования',
        validators=[
            InputRequired(message='Обязательное поле')
        ]
    )
    rests_at = DateField(
        label='Время окончания периода бодрствования',
        validators=[
            InputRequired(message='Обязательное поле'),
            LaterThanOrAt(message='Время окончания периода бодрствования должно быть позже или равно '
                                  'времени начала периода бодрствования',
                          fieldname='awakens_at')
        ]
    )
    visits = FieldList(
        label='Места для посещения',
        unbound_field=FormField(VisitForm),
        validators=[
            MinimalLength(minimum=1, message='Хотя бы одно место должно быть выбрано')
        ]
    )
