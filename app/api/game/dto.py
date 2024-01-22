from flask_restx import Namespace, fields


class TurnDto:
    api = Namespace("turn", description="Turn related operations.")
    turn = api.model(
        "Turn object",
        {
            "game_id": fields.Integer,
            "player_id": fields.Integer,
            "row": fields.Integer,
            "col": fields.Integer,
        },
    )

    data_resp = api.model(
        "Turn Data Response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "turn": fields.Nested(turn),
        },
    )


class GameBoardDto:
    api = Namespace("game", description="Game related operations.")
    data_resp = api.model(
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
