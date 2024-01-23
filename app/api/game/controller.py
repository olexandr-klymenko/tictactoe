from flask_restx import Resource, reqparse

from .dto import GameDto
from .service import GameService

ns = GameDto.api
start_game_in = GameDto.start_game_in
start_game_out = GameDto.start_game_out
view_board = GameDto.view_board
turn_data = GameDto.turn_data
game_stat = GameDto.game_stat


@ns.route("/<string:game_id>")
class Game(Resource):
    @ns.doc("view_board")
    @ns.marshal_with(view_board)
    def get(self, game_id):
        """Get a specific game data by its id"""
        return GameService.view_board(game_id)

    @ns.doc(
        "make_turn",
        responses={
            200: ("Game data successfully sent", turn_data),
            400: "Invalid turn",
            403: "Player not in the game of not player's turn",
            404: "Game not found",
            409: "Game is finished or cell is taken",
        },
    )
    @ns.expect(turn_data)
    @ns.marshal_with(turn_data)
    def put(self, game_id):
        """Make a turn"""
        return GameService.make_turn(game_id=game_id, turn=ns.payload)


@ns.route("/")
class Games(Resource):
    @ns.doc("start_game")
    @ns.expect(start_game_in)
    @ns.marshal_with(start_game_out)
    def post(self):
        """Start a tic-tac-toe game"""
        return GameService.start_game(data=ns.payload)

    @ns.doc("list_games")
    @ns.marshal_list_with(game_stat)
    def get(self):
        """List games"""
        parser = reqparse.RequestParser()
        parser.add_argument("season_id", type=int, location="args")
        parser.add_argument("player_id", type=int, location="args")
        parser.add_argument("is_draw", type=bool, location="args")
        args = parser.parse_args()
        return GameService.list_games(**args)
