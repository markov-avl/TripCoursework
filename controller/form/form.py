from flask_wtf import FlaskForm


class Form(FlaskForm):
    class Meta:
        csrf = False

    _TRANSLATIONS = {
        'Not a valid integer value.': 'Поле должно быть целым числом'
    }

    @property
    def extended_errors(self) -> list[str]:
        extended_errors: list[str] = []
        for field, messages in self.errors.items():
            errors = '; '.join(self._TRANSLATIONS.get(message, message).lower() for message in set(messages))
            extended_errors.append(f'{self[field].label.text}: {errors}')
        return extended_errors
