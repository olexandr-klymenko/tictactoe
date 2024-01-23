from app import db
from app.api.admin.service import AdminService
from app.api.game.service import GameService
from app.models.models import GameModel, PlayerModel
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

    def test_list_seasons(self):
        self.create_players_season_game()
        self.create_players_season_game(
            player_x_name="Test Player 3",
            player_x_email="test3@example.com",
            player_o_name="Test Player 4",
            player_o_email="test4@example.com",
            season_name="Test season 2",
        )
        self.create_players_season_game(
            player_x_name="Test Player 5",
            player_x_email="test5@example.com",
            player_o_name="Test Player 6",
            player_o_email="test6@example.com",
            season_name="Test season 3",
        )
        self.assertEqual(
            AdminService.list_seasons(),
            [
                {"season_id": 3, "season_name": "Test season 3"},
                {"season_id": 2, "season_name": "Test season 2"},
                {"season_id": 1, "season_name": "Test season 1"},
            ],
        )

    def test_ranking_table(self):
        # create data for the first game with winner player_x
        player_x, player_o, season, game = self.create_players_season_game()
        game.winner_id = player_x.id
        db.session.commit()

        # create data for the second game with winner player_3
        player_3 = PlayerModel(name="Test Player 3", email="test3@example.com")
        db.session.add(player_3)
        db.session.commit()

        game2 = GameModel(
            player_x_id=player_x.id,
            player_o_id=player_3.id,
            season_id=season.id,
        )
        game2.winner_id = player_x.id

        # create data for the third game with winner player_3
        game3 = GameModel(
            player_x_id=player_3.id,
            player_o_id=player_o.id,
            season_id=season.id,
        )
        game3.winner_id = player_3.id
        db.session.add_all([game2, game3])
        db.session.commit()

        resp = AdminService.ranking_table()
        self.assertEqual(
            resp,
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
            ],
        )
