from flask_restx import Resource
from flask_restx import Namespace, fields

from app.models.schemas import ListPlayersSchema
from .service import AdminService


ns = Namespace("admin", description="Management related operations.")
start_season_in = ns.model(
    "Start new league season request",
    {
        "name": fields.String,
    },
    strict=True,
)

start_season_out = ns.model(
    "Start new league season response",
    {
        "name": fields.String,
        "season_id": fields.Integer,
    },
)
create_player_in = ns.model(
    "Create player request",
    {
        "name": fields.String(required=True),
        "email": fields.String(required=True),
        "age": fields.Integer,
        "country": fields.String,
    },
    strict=True,
)

player_out = ns.model(
    "Player response",
    {
        "id": fields.Integer,
        "name": fields.String,
        "email": fields.String,
        "age": fields.Integer,
        "country": fields.String,
    },
)

player = ns.model(
    "Player details",
    {
        "id": fields.Integer,
        "name": fields.String,
        "email": fields.String,
        "age": fields.Integer,
        "country": fields.String,
    },
)


@ns.route("/seasons/")
class Seasons(Resource):
    @ns.doc("start_season")
    @ns.expect(start_season_in)
    @ns.marshal_with(start_season_out, code=201)
    def post(self):
        """Start new league season"""
        return AdminService.start_season(data=ns.payload)

    @ns.doc("list_seasons")
    @ns.marshal_list_with(start_season_out)
    def get(self):
        """List all league seasons"""
        return AdminService.list_seasons()


@ns.route("/ranking/")
class RankingTable(Resource):
    """Endpoint for rendering ranking table"""

    @ns.doc("ranking_table")
    def get(self):
        return AdminService.ranking_table()


@ns.route("/players/")
class Players(Resource):
    @ns.doc("create_player")
    @ns.expect(create_player_in)
    @ns.marshal_with(player_out)
    def post(self):
        """Create player"""
        return AdminService.create_player(data=ns.payload)

    @ns.doc("list_players")
    def get(self):
        """List players"""
        return (
            ListPlayersSchema(many=True).dump(AdminService.list_players()),
            200,
        )


@ns.route("/players/<string:id>")
class Player(Resource):
    @ns.doc("get_player")
    @ns.marshal_with(player_out)
    def get(self, id):
        """Get player details"""
        return AdminService.get_player(id)

    @ns.doc("delete_players")
    def delete(self, id):
        """Delete player"""
        return AdminService.delete_player(id)
