from flask_restx import Namespace, fields


class AdminDto:
    api = Namespace("admin", description="Management related operations.")
    start_season_in = api.model(
        "Start new league season request",
        {
            "name": fields.String,
        },
    )

    start_season_out = api.model(
        "Start new league season response",
        {
            "name": fields.String,
            "season_id": fields.Integer,
        },
    )
