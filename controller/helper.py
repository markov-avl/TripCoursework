from typing import Type, Any

import flask
from flask import flash

from .form import Form

translations = {
    'Not a valid integer value.': 'Поле должно быть целым числом'
}


def redirect() -> flask.Response:
    return flask.redirect(flask.request.values.get('redirect', flask.url_for('index.index')))


def get_form(form_type: Type[Form]) -> Form | Any:
    fr = flask.request
    return form_type(flask.request.form) if flask.request.form else form_type.from_json(flask.request.json)


def flash_message(text: str) -> None:
    flash(text, 'green')


def flash_warning(text: str) -> None:
    flash(text, 'yellow')


def flash_errors(errors: list[str]) -> None:
    for error in errors:
        flash_warning(error)


def flash_form_errors(form: Form) -> None:
    flash_errors(form.extended_errors)


def get_response(status_code: int, **json) -> flask.Response:
    response = flask.jsonify(**json)
    response.status_code = status_code
    return response


def ok(**json) -> flask.Response:
    return get_response(200, **json)


def created(**json) -> flask.Response:
    return get_response(201, **json)


def no_content() -> flask.Response:
    return get_response(204)


def bad_request(**json) -> flask.Response:
    return get_response(400, **json)


def unprocessable_content(**json) -> flask.Response:
    return get_response(422, **json)
