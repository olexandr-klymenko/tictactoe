from flask_restx import Namespace, fields


class GameDto:
    api = Namespace("game", description="Game related operations.")
    view_board = api.model(
        "Game board object",
        {
            "player_x": fields.String,
            "player_o": fields.String,
            "current_player": fields.String,
            "winner": fields.String,
            "board": fields.List(fields.List(fields.String)),
        },
    )

    start_game_in = api.model(
        "Start tic-tac-toe game request",
        {
            "player_x_id": fields.Integer,
            "player_o_id": fields.Integer,
        },
    )

    start_game_out = api.model(
        "Start tic-tac-toe game response",
        {"game_id": fields.Integer},
    )

    turn_data = api.model(
        "Turn object",
        {
            "player_id": fields.Integer,
            "row": fields.Integer,
            "col": fields.Integer,
        },
    )
