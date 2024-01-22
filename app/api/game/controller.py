from flask_restx import Resource

from .service import GameBoardService
from .dto import GameBoardDto

ns = GameBoardDto.api
data_resp = GameBoardDto.data_resp
start_game = GameBoardDto.start_game_in
turn = GameBoardDto.turn_in


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

    @ns.doc(
        "Make a turn",
        responses={
            200: ("Game data successfully sent", turn),
            400: "Invalid turn",
            403: "Player not in the game of not player's turn",
            404: "Game not found",
            409: "Game is finished or cell is taken",
        },
    )
    @ns.expect(turn)
    def put(self, game_id):
        """Get a specific game data by its id"""
        return GameBoardService.make_turn(game_id=game_id, turn=ns.payload)


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
        """Start a tic-tac-toe game"""
        return GameBoardService.start_game(data=ns.payload)
