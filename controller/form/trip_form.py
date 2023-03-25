from wtforms import IntegerField, DateField, FieldList, FormField, TimeField
from wtforms.validators import InputRequired

from .visit_form import VisitForm
from .validator import LaterThanOrAt, MinimalLength

from .form import Form


class TripForm(Form):
    city_id = IntegerField(
        label='Город',
        validators=[
            InputRequired(message='Обязательное поле')
        ]
    )
    accommodation_id = IntegerField(
        label='Ночлег',
        validators=[
            InputRequired(message='Обязательное поле')
        ]
    )
    starts_at = DateField(
        label='Дата начала путешествия',
        validators=[
            InputRequired(message='Обязательное поле')
        ],
        format=['%Y-%m-%d', '%d.%m.%Y']
    )
    ends_at = DateField(
        label='Дата окончания путешествия',
        validators=[
            InputRequired(message='Обязательное поле'),
            LaterThanOrAt(message='Дата окончания путешествия должна быть позже или равна '
                                  'дате начала',
                          fieldname='starts_at')
        ],
        format=['%Y-%m-%d', '%d.%m.%Y']
    )
    awakens_at = TimeField(
        label='Время начала периода бодрствования',
        validators=[
            InputRequired(message='Обязательное поле')
        ]
    )
    rests_at = TimeField(
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
