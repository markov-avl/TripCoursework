from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import FieldList


class Form(FlaskForm):
    class Meta:
        csrf = False

    _TRANSLATIONS = {
        'Not a valid integer value.': 'Поле должно быть целым числом',
        'Not a valid date value.': 'Невалидный формат',
        'Not a valid time value.': 'Невалидный формат',
        'This field is required.': 'Обязательное поле'
    }

    @property
    def extended_errors(self) -> list[str]:
        return self._get_extended_errors_from_dict(self)

    def _get_extended_errors_from_dict(self, form: Form, prefix: str = '') -> list[str]:
        extended_errors: list[str] = []

        for field, messages in form.errors.items():
            if messages and isinstance(messages[0], dict):
                extended_errors.extend(self._get_extended_errors_from_list(form[field]))
            else:
                errors = '; '.join(self._TRANSLATIONS.get(message, message).lower() for message in set(messages))
                extended_errors.append(f'{prefix}{form[field].label.text}: {errors}')

        return extended_errors

    def _get_extended_errors_from_list(self, form: FieldList) -> list[str]:
        extended_errors: list[str] = []

        for i, entry in enumerate(form.entries):
            extended_errors.extend(self._get_extended_errors_from_dict(entry.form, f'{i + 1}. [{form.label.text}] '))

        return extended_errors
