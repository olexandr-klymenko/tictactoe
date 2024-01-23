from flask import current_app

from app import db
from app.models.models import SeasonModel
from app.models.schemas import SeasonStartSchema
from app.utils import internal_err_resp, message


class AdminService:
    @staticmethod
    def start_season(data):
        try:
            season = SeasonModel(name=data["name"])
            db.session.add(season)
            db.session.commit()
            data = SeasonStartSchema().dump(season)
            resp = message(True, f"Season '{season.name}' started")
            resp["data"] = data
            return resp, 201

        except Exception as error:
            db.session.rollback()
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def ranking_table(season_id=None):
        if not season_id:
            season_id = SeasonModel.current_season_id()
