from flask_restx import Resource

from .service import GameBoardService
from .dto import TurnDto

api = TurnDto.api
data_resp = TurnDto.data_resp


@api.route("/<string:game_id>")
class GameBoardGet(Resource):
    @api.doc(
        "Get a specific user",
        responses={
            200: ("User data successfully sent", data_resp),
            404: "User not found!",
        },
    )
    def get(self, username):
        """Get a specific user's data by their username"""
        return GameBoardService.view_board(username)
