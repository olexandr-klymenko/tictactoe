from flask_restx import Resource

from .service import GameBoardService
from .dto import GameBoardDto

ns = GameBoardDto.api
data_resp = GameBoardDto.data_resp
start_game = GameBoardDto.start_game_in


@ns.route("/<string:game_id>")
class GameBoard(Resource):
    @ns.doc(
        "View the game board",
        responses={
            200: ("Game data successfully sent", data_resp),
            404: "Game not found!",
        },
    )
    def get(self, game_id):
        """Get a specific game data by its id"""
        return GameBoardService.view_board(game_id)


@ns.route("/")
class GameStart(Resource):
    @ns.doc(
        "Start the game",
        responses={
            201: ("Game successfully started", data_resp),
            400: "Invalid data!",
        },
    )
    @ns.expect(start_game)
    def post(self):
        """Start tic-tac-toe game"""
        return GameBoardService.start_game(data=ns.payload)
