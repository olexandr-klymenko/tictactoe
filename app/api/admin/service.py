from typing import List, Dict

from flask import current_app
from sqlalchemy import and_, case, func, or_

from app import db
from app.models.models import (
    GameModel,
    PlayerModel,
    SeasonModel,
    GameTurnModel,
)
from app.models.schemas import (
    RankingRecordSchema,
    PlayerSchema,
    ListPlayersSchema,
)
from app.utils import internal_err_resp, err_resp

list_player_schema = ListPlayersSchema(many=True)


class AdminService:
    @staticmethod
    def create_player(data):
        """Create player"""
        player = PlayerModel(**data)
        db.session.add(player)
        db.session.commit()
        return PlayerSchema().dump(player), 201

    @staticmethod
    def get_player(player_id):
        """Get player by player_id"""
        player = PlayerModel.query.filter(PlayerModel.id == player_id).first()
        if not player:
            return err_resp("Player not found", "player_404", 404)
        return PlayerSchema().dump(player), 200

    @staticmethod
    def delete_player(player_id):
        """Delete player by player_id"""
        player = PlayerModel.query.filter(PlayerModel.id == player_id).first()
        if not player:
            return err_resp("Player not found", "player_404", 404)
        player_turns = GameTurnModel.query.filter(
            GameTurnModel.player_id == player_id
        ).all()
        if player_turns:
            return err_resp(
                "There are games that player participated in",
                "player_409",
                409,
            )
        db.session.delete(player)
        db.session.commit()
        return None, 204

    @staticmethod
    def list_players():
        """List all players"""
        return PlayerModel.query.all()

    @staticmethod
    def start_season(data):
        """
        Start new league season.
        (Sets current season id to this one's id).
        """
        try:
            season = SeasonModel(name=data["name"])
            db.session.add(season)
            db.session.commit()
            return {"name": data["name"], "season_id": season.id}, 201

        except Exception as error:
            db.session.rollback()
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def list_seasons() -> List[Dict]:
        """
        List of league seasons from the current one to the oldest.
        """
        seasons_query = (
            db.session.query(SeasonModel.id, SeasonModel.name)
            .order_by(SeasonModel.id.desc())
            .all()
        )
        return [
            {"season_id": season_id, "name": season_name}
            for season_id, season_name in seasons_query
        ]

    @staticmethod
    def ranking_table(season_id: int = None):
        """
        Build ranking table for given season.
        If season_id is not set build table for current season.
        Players that didn't play in the season don't showed in the table.

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
                {
                    "rank": rank,
                    "player_id": player_id,
                    "player_name": player_name,
                    "total_points": total_points,
                }
            )
        return RankingRecordSchema(many=True).dump(resp), 200
