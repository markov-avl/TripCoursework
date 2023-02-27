import flask


def redirect() -> flask.Response:
    return flask.redirect(flask.request.values.get('redirect', flask.url_for('index.index')))
