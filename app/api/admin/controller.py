from flask_restx import Resource

from .dto import AdminDto
from .service import AdminService

ns = AdminDto.api
start_season_in = AdminDto.start_season_in
start_season_out = AdminDto.start_season_out


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
