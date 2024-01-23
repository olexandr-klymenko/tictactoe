from typing import List

from flask import current_app
from sqlalchemy import func, case, or_, and_

from app import db
from app.models.models import SeasonModel, PlayerModel, GameModel
from app.models.schemas import (
    SeasonStartSchema,
    RankingRecordSchema,
    SeasonSchema,
)
from app.utils import internal_err_resp, message


class AdminService:
    @staticmethod
    def create_player(data):
        """"""

    @staticmethod
    def delete_player(player_id):
        """"""

    @staticmethod
    def get_player(player_id):
        """"""

    @staticmethod
    def start_season(data):
        """
        Start new league season.
        Set current season id to this one.
        Args:
            data:

        Returns:

        """
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
    def list_seasons() -> List[SeasonSchema]:
        """
        List of league seasons from the current one to the oldest.
        """
        seasons_query = (
            db.session.query(SeasonModel.id, SeasonModel.name)
            .order_by(SeasonModel.id.desc())
            .all()
        )
        return [
            SeasonSchema().dump(
                {"season_id": season_id, "season_name": season_name}
            )
            for season_id, season_name in seasons_query
        ]

    @staticmethod
    def ranking_table(season_id: int = None) -> List[RankingRecordSchema]:
        """
        Build ranking table for given season.
        If season_id is not set build table for current season.
        Players that didn't play in the season don't showed in the table.
        Args:
            season_id:
        Returns:
            List of RankingRecordSchema
        Examples:
            [
                {
                    "player_id": 1,
                    "player_name": "Test Player 1",
                    "rank": 1,
                    "total_points": 4,
                },
                {
                    "player_id": 3,
                    "player_name": "Test Player 3",
                    "rank": 2,
                    "total_points": 3,
                },
                {
                    "player_id": 2,
                    "player_name": "Test Player 2",
                    "rank": 3,
                    "total_points": 2,
                },
            ]

        """
        if not season_id:
            season_id = SeasonModel.current_season_id()

        # predefine total_points_expr column
        total_points_expr = func.sum(
            case(
                (
                    GameModel.winner_id == PlayerModel.id,
                    2,
                ),  # Wins count as 2 points
                (GameModel.winner_id.is_(None), 0),  # Draws count as 0 point
                (
                    and_(
                        GameModel.winner_id != PlayerModel.id,
                    ),
                    1,
                ),  # Losses count as 1 point
            )
        ).label("total_points")

        ranking_query = (
            db.session.query(
                PlayerModel.id, PlayerModel.name, total_points_expr
            )
            .filter(GameModel.season_id == season_id)
            .join(
                GameModel,
                or_(
                    PlayerModel.id == GameModel.player_x_id,
                    PlayerModel.id == GameModel.player_o_id,
                ),
            )
            .group_by(PlayerModel.id, PlayerModel.name)
            .order_by(total_points_expr.desc())
        )

        ranking_results = ranking_query.all()

        resp = []
        for rank, (player_id, player_name, total_points) in enumerate(
            ranking_results, start=1
        ):
            resp.append(
                RankingRecordSchema().dump(
                    {
                        "rank": rank,
                        "player_id": player_id,
                        "player_name": player_name,
                        "total_points": total_points,
                    }
                )
            )
        return resp
