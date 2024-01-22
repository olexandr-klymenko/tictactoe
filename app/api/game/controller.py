from flask_restx import Resource

from .dto import GameBoardDto
from .service import GameService

ns = GameBoardDto.api
start_game = GameBoardDto.start_game_in
view_board = GameBoardDto.view_board
turn_data = GameBoardDto.turn_data


@ns.route("/<string:game_id>")
class Game(Resource):
    @ns.doc(
        "View the game board",
        responses={
            200: ("Game data successfully sent", view_board),
            404: "Game not found!",
        },
    )
    def get(self, game_id):
        """Get a specific game data by its id"""
        return GameService.view_board(game_id)

    @ns.doc(
        "Make a turn",
        responses={
            200: ("Game data successfully sent", turn_data),
            400: "Invalid turn",
            403: "Player not in the game of not player's turn",
            404: "Game not found",
            409: "Game is finished or cell is taken",
        },
    )
    @ns.expect(turn_data)
    def put(self, game_id):
        """Make a turn"""
        return GameService.make_turn(game_id=game_id, turn=ns.payload)


@ns.route("/")
class Games(Resource):
    @ns.doc(
        "Start the game",
        responses={
            201: ("Game successfully started", view_board),
            400: "Invalid data!",
        },
    )
    @ns.expect(start_game)
    def post(self):
        """Start a tic-tac-toe game"""
        return GameService.start_game(data=ns.payload)
