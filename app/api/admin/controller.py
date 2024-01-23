from flask_restx import Resource

from app.models.schemas import ListPlayersSchema
from .dto import AdminDto
from .service import AdminService

ns = AdminDto.api
start_season_in = AdminDto.start_season_in
start_season_out = AdminDto.start_season_out
create_player_in = AdminDto.create_player_in
player_out = AdminDto.player_out
player = AdminDto.player


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
