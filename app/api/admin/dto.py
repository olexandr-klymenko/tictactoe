from flask_restx import Namespace, fields


class AdminDto:
    api = Namespace("admin", description="Management related operations.")
    start_season_in = api.model(
        "Start new league season request",
        {
            "name": fields.String,
        },
        strict=True,
    )

    start_season_out = api.model(
        "Start new league season response",
        {
            "name": fields.String,
            "season_id": fields.Integer,
        },
    )
    create_player_in = api.model(
        "Create player request",
        {
            "name": fields.String(required=True),
            "email": fields.String(required=True),
            "age": fields.Integer,
            "country": fields.String,
        },
        strict=True,
    )

    player_out = api.model(
        "Player response",
        {
            "id": fields.Integer,
            "name": fields.String,
            "email": fields.String,
            "age": fields.Integer,
            "country": fields.String,
        },
    )

    player = api.model(
        "Player details",
        {
            "id": fields.Integer,
            "name": fields.String,
            "email": fields.String,
            "age": fields.Integer,
            "country": fields.String,
        },
    )
