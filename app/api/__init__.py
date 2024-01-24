from flask import Blueprint
from flask_restx import Api

# Import controller APIs as namespaces.
from .game.controller import ns as game_ns
from .admin.controller import ns as admin_ns


api_bp = Blueprint("api", __name__)

api = Api(
    api_bp,
    version="1.0",
    title="Tic-tac-toe game API",
    description="An API for playing Tic-tac-toe game",
)

# API namespaces
api.add_namespace(game_ns)
api.add_namespace(admin_ns)
