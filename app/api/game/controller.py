from flask_restx import Resource, reqparse, Namespace, fields

from .service import GameService

ns = Namespace("games", description="Game related operations.")
view_board = ns.model(
    "Game board object",
    {
        "player_x": fields.String,
        "player_o": fields.String,
        "current_player": fields.String,
        "winner": fields.String,
        "board": fields.List(fields.List(fields.String)),
    },
)

start_game_in = ns.model(
    "Start tic-tac-toe game request",
    {
        "player_x_id": fields.Integer,
        "player_o_id": fields.Integer,
    },
)

start_game_out = ns.model(
    "Start tic-tac-toe game response",
    {"game_id": fields.Integer},
)

game_stat = ns.model(
    "Game statistic response",
    {
        "season_id": fields.Integer,
        "game_id": fields.Integer,
        "player_x": fields.String,
        "player_o": fields.String,
        "winner": fields.String,
        "turns": fields.Integer,
    },
)

turn_data = ns.model(
    "Turn object",
    {
        "player_id": fields.Integer,
        "row": fields.Integer,
        "col": fields.Integer,
    },
)


@ns.route("/<string:game_id>")
@ns.response(404, "Game not found")
class Game(Resource):
    @ns.doc("view_board")
    @ns.marshal_with(view_board)
    def get(self, game_id):
        """Get a specific game data by its id"""
        return GameService.view_board(game_id)

    @ns.doc("make_turn")
    @ns.response(400, "Invalid turn")
    @ns.response(403, "Player not in the game of not player's turn")
    @ns.response(409, "Game is finished or cell is taken")
    @ns.expect(turn_data)
    @ns.marshal_with(turn_data)
    def put(self, game_id):
        """Make a turn"""
        return GameService.make_turn(game_id=game_id, turn=ns.payload)


@ns.route("/")
class Games(Resource):
    @ns.doc("start_game")
    @ns.response(400, "Invalid game data")
    @ns.response(404, "Player not found")
    @ns.expect(start_game_in)
    @ns.marshal_with(start_game_out)
    def post(self):
        """Start a tic-tac-toe game"""
        return GameService.start_game(data=ns.payload)

    @ns.doc("list_games")
    @ns.marshal_list_with(game_stat)
    def get(self):
        """List games"""

        # Define query arguments
        parser = reqparse.RequestParser()
        parser.add_argument(
            "season_id", type=int, location="args"
        )  # filter by season
        parser.add_argument(
            "player_id", type=int, location="args"
        )  # filter by player
        parser.add_argument(
            "is_draw", type=bool, location="args"
        )  # filter by game draw
        args = parser.parse_args()

        return GameService.list_games(**args)
