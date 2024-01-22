from flask import Blueprint
from flask_restx import Api

from .game.controller import ns as game_ns

# Import controller APIs as namespaces.
api_bp = Blueprint("api", __name__)

api = Api(api_bp, title="API", description="Main routes.")

# API namespaces
api.add_namespace(game_ns)
