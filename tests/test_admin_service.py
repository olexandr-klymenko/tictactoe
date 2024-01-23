from app.api.admin.service import AdminService
from app.api.game.service import GameService
from app.models.models import GameModel
from tests.utils.base import BaseTestCase


class TestAdminService(BaseTestCase):
    def test_start_season(self):
        """
        Check that game created after new season started has new season id.
        """
        player_x, player_o, season, game = self.create_players_season_game()
        resp = AdminService.start_season(data={"name": "New season"})
        self.assertEqual(
            resp,
            (
                {
                    "data": {"name": "New season"},
                    "message": "Season 'New season' started",
                    "status": True,
                },
                201,
            ),
        )
        resp = GameService.start_game(
            data={
                "player_x_id": player_x.id,
                "player_o_id": player_o.id,
            }
        )
        retrieved_game = GameModel.query.filter_by(
            id=resp[0]["data"]["game_id"]
        ).first()
        self.assertTrue(
            retrieved_game.player_x_id == player_x.id
            and retrieved_game.player_o_id == player_o.id
            and retrieved_game.season_id > season.id
        )
