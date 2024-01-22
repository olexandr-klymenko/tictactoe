from flask_restx import Namespace, fields


class UserDto:
    api = Namespace("user", description="User related operations.")
    user = api.model(
        "User object",
        {
            "email": fields.String,
            "name": fields.String,
            "username": fields.String,
            "joined_date": fields.DateTime,
            "role_id": fields.Integer,
        },
    )

    data_resp = api.model(
        "User Data Response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "user": fields.Nested(user),
        },
    )


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
