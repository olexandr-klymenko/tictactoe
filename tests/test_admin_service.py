import werkzeug

from app import db
from app.api.admin.service import AdminService
from app.api.game.service import GameService
from app.models import GameModel, PlayerModel
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
                {"name": "New season", "season_id": 2},
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
            id=resp[0]["game_id"]
        ).first()
        self.assertTrue(
            retrieved_game.player_x_id == player_x.id
            and retrieved_game.player_o_id == player_o.id
            and retrieved_game.season_id > season.id
        )

    def test_list_seasons(self):
        # prepare test data
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
                {"season_id": 3, "name": "Test season 3"},
                {"season_id": 2, "name": "Test season 2"},
                {"season_id": 1, "name": "Test season 1"},
            ],
        )

    def test_ranking_table(self):
        self.create_some_games()

        resp = AdminService.ranking_table()
        self.assertEqual(
            resp,
            (
                (
                    [
                        {
                            "player_id": 2,
                            "player_name": "Test player 2",
                            "rank": 1,
                            "total_points": 3,
                        },
                        {
                            "player_id": 1,
                            "player_name": "Test player 1",
                            "rank": 2,
                            "total_points": 2,
                        },
                        {
                            "player_id": 3,
                            "player_name": "Test player 3",
                            "rank": 3,
                            "total_points": 1,
                        },
                    ],
                    200,
                )
            ),
        )

    def test_create_player(self):
        resp = AdminService.create_player(
            {
                "name": "Test Player",
                "email": "test@example.com",
                "age": 18,
                "country": "US",
            }
        )
        self.assertEqual(
            resp,
            (
                {
                    "age": 18,
                    "country": "US",
                    "email": "test@example.com",
                    "name": "Test Player",
                    "id": 1,
                },
                201,
            ),
        )
        retrieved_player = PlayerModel.query.first()
        self.assertEqual(retrieved_player.email, "test@example.com")

    def test_get_player(self):
        player = PlayerModel(
            name="Test Player", email="test@example.com", age=20, country="UK"
        )
        db.session.add(player)
        db.session.commit()

        resp = AdminService.get_player(player.id)
        self.assertEqual(
            resp,
            (
                {
                    "age": 20,
                    "country": "UK",
                    "email": "test@example.com",
                    "id": 1,
                    "name": "Test Player",
                },
                200,
            ),
        )

    def test_get_player_not_found(self):
        with self.assertRaises(werkzeug.exceptions.NotFound):
            AdminService.get_player(999)

    def test_delete_player(self):
        player = PlayerModel(
            name="Test Player", email="test@example.com", age=20, country="UK"
        )
        db.session.add(player)
        db.session.commit()

        resp = AdminService.delete_player(player.id)
        self.assertEqual(
            resp,
            (
                None,
                204,
            ),
        )

    def test_delete_player_fail(self):
        player, _, __, ___ = self.create_players_season_game()
        with self.assertRaises(werkzeug.exceptions.Conflict):
            AdminService.delete_player(player.id)
