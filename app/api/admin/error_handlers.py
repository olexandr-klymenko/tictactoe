import werkzeug

from app.api.game.controller import ns


@ns.errorhandler(werkzeug.exceptions.BadRequest)
def bad_request_error_handler(error):
    return {"message": str(error)}, 400


@ns.errorhandler(werkzeug.exceptions.NotFound)
def not_found_error_handler(error):
    return {"message": str(error)}, 404


@ns.errorhandler(werkzeug.exceptions.Conflict)
def conflict_error_handler(error):
    return {"message": str(error)}, 409
