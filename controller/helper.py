from typing import Type

import flask
from flask import flash
from flask_wtf import FlaskForm

translations = {
    'Not a valid integer value.': 'Поле должно быть целым числом'
}


def redirect() -> flask.Response:
    return flask.redirect(flask.request.values.get('redirect', flask.url_for('index.index')))


def get_form(form_type: Type[FlaskForm]) -> FlaskForm:
    return form_type(flask.request.form) if flask.request.form else form_type(data=flask.request.json)


def flash_message(text: str) -> None:
    flash(text, 'message')


def flash_warning(text: str) -> None:
    flash(text, 'warning')


def flash_form_errors(form: FlaskForm) -> None:
    for field, messages in form.errors.items():
        errors = '; '.join(translations.get(message, message).lower() for message in set(messages))
        flash_warning(f'{form[field].label.text}: {errors}.')
