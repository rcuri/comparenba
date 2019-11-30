from flask import render_template, request
from app import db
from app.errors import bp
from app.api.errors import error_response as api_error_response


def wants_json_response():
    """
    Compares preference for JSON or HTML selected by client in their list of
    preferred formats.
    """
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


@bp.app_errorhandler(404)
def not_found_error(error):
    """
    Returns 404 error code in JSON or HTML response for 404 error code,
    depending on client preference.
    """
    if wants_json_response():
        return api_error_response(404)
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    """
    Returns 500 error code in JSON or HTML response, depending on client
    preference.
    """
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template('errors/500.html'), 500
