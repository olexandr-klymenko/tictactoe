from flask import Blueprint
from flask_restx import Api

# Import controller APIs as namespaces.
from .game.controller import ns as game_ns
from .admin.controller import ns as admin_ns


api_bp = Blueprint("api", __name__)

api = Api(api_bp, title="API", description="Tic-tac-toe game API")

# API namespaces
api.add_namespace(game_ns)
api.add_namespace(admin_ns)
