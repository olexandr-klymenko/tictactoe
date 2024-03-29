import werkzeug

from app import db
from app.api.game.service import GameService
from app.models import (
    GameModel,
    TurnModel,
    PlayerModel,
    SeasonModel,
)
from tests.utils.base import BaseTestCase


class TestGameService(BaseTestCase):
    def test_start_game(self):
        player_x = PlayerModel(name="Test Player 1", email="test1@example.com")
        player_o = PlayerModel(name="Test Player 2", email="test2@example.com")
        season = SeasonModel(name="Test season")
        db.session.add_all([player_x, player_o, season])
        db.session.commit()

        resp = GameService.start_game(
            data={
                "player_x_id": player_x.id,
                "player_o_id": player_o.id,
            }
        )
        self.assertEquals(
            resp,
            (
                {"game_id": 1},
                201,
            ),
        )
        retrieved_game = GameModel.query.first()
        self.assertTrue(
            retrieved_game.player_x_id == player_x.id
            and retrieved_game.player_o_id == player_o.id
            and retrieved_game.season_id == season.id
        )

    def test_list_games_all(self):
        self.create_some_games()
        resp = GameService.list_games()
        self.assertEquals(
            resp,
            (
                [
                    {
                        "season_id": 1,
                        "game_id": 1,
                        "player_x": "Test player 1",
                        "player_o": "Test player 2",
                        "winner": "Test player 1",
                        "turns": 0,
                    },
                    {
                        "season_id": 1,
                        "game_id": 2,
                        "player_x": "Test player 2",
                        "player_o": "Test player 3",
                        "winner": "Test player 2",
                        "turns": 0,
                    },
                    {
                        "season_id": 1,
                        "game_id": 3,
                        "player_x": "Test player 1",
                        "player_o": "Test player 3",
                        "winner": None,
                        "turns": 0,
                    },
                ],
                200,
            ),
        )

    def test_list_games_draw(self):
        self.create_some_games()
        resp = GameService.list_games(is_draw=False)
        self.assertEquals(
            resp,
            (
                [
                    {
                        "season_id": 1,
                        "game_id": 1,
                        "player_x": "Test player 1",
                        "player_o": "Test player 2",
                        "winner": "Test player 1",
                        "turns": 0,
                    },
                    {
                        "season_id": 1,
                        "game_id": 2,
                        "player_x": "Test player 2",
                        "player_o": "Test player 3",
                        "winner": "Test player 2",
                        "turns": 0,
                    },
                ],
                200,
            ),
        )

    def test_view_board(self):
        player_x, player_o, season, game = self.create_players_season_game()

        turns = [
            TurnModel(player_id=player_x.id, row=0, col=0, game_id=game.id),
            TurnModel(player_id=player_o.id, row=1, col=1, game_id=game.id),
            TurnModel(player_id=player_x.id, row=0, col=1, game_id=game.id),
            TurnModel(player_id=player_o.id, row=0, col=2, game_id=game.id),
            TurnModel(player_id=player_x.id, row=1, col=0, game_id=game.id),
            TurnModel(player_id=player_o.id, row=2, col=0, game_id=game.id),
        ]
        db.session.add_all(turns)
        db.session.commit()
        resp = GameService.view_board(game.id)
        self.assertEquals(
            resp,
            (
                {
                    "player_x": "Test Player 1",
                    "player_o": "Test Player 2",
                    "current_player": "Test Player 1",
                    "winner": None,
                    "board": [
                        ["X", "X", "O"],
                        ["X", "O", "_"],
                        ["O", "_", "_"],
                    ],
                },
                200,
            ),
        )

    def test_start_game_fail_no_player_o(self):
        player_x = PlayerModel(name="Test Player 1", email="test1@example.com")
        season = SeasonModel(name="Test season")
        db.session.add_all([player_x, season])
        db.session.commit()

        with self.assertRaises(werkzeug.exceptions.NotFound):
            GameService.start_game(
                data={
                    "player_x_id": player_x.id,
                    "player_o_id": 999,
                }
            )

    def test_start_game_fail_two_same_players(self):
        player_x = PlayerModel(name="Test Player 1", email="test1@example.com")
        season = SeasonModel(name="Test season")
        db.session.add_all([player_x, season])
        db.session.commit()

        with self.assertRaises(werkzeug.exceptions.BadRequest):
            GameService.start_game(
                data={
                    "player_x_id": player_x.id,
                    "player_o_id": player_x.id,
                }
            )

    def test_make_turn_game_not_found(self):
        with self.assertRaises(werkzeug.exceptions.NotFound):
            GameService.make_turn(
                game_id=999,
                turn={
                    "player_id": 1,
                    "row": 0,
                    "col": 0,
                },
            )

    def test_make_turn_game_finished(self):
        player_x, player_o, season, game = self.create_players_season_game()
        game.winner_id = player_x.id
        db.session.add(game)
        db.session.commit()

        with self.assertRaises(werkzeug.exceptions.Conflict):
            GameService().make_turn(
                game_id=game.id,
                turn={
                    "player_id": player_x.id,
                    "row": 0,
                    "col": 0,
                },
            )

    def test_make_turn_not_authorized(self):
        player_x = PlayerModel(name="Test Player 1", email="test1@example.com")
        player_o = PlayerModel(name="Test Player 2", email="test2@example.com")
        player_i = PlayerModel(name="Test Player 3", email="test3@example.com")
        season = SeasonModel(name="Test season")
        db.session.add_all([player_x, player_o, player_i, season])
        db.session.commit()

        game = GameModel(
            player_x_id=player_x.id,
            player_o_id=player_o.id,
            season_id=season.id,
        )
        db.session.add(game)
        db.session.commit()

        with self.assertRaises(werkzeug.exceptions.Unauthorized):
            GameService().make_turn(
                game_id=game.id,
                turn={
                    "player_id": player_i.id,
                    "row": 0,
                    "col": 0,
                },
            )

    def test_make_turn_not_current_player(self):
        player_x, player_o, season, game = self.create_players_season_game()
        with self.assertRaises(werkzeug.exceptions.Forbidden):
            GameService().make_turn(
                game_id=game.id,
                turn={
                    "player_id": player_o.id,
                    "row": 0,
                    "col": 0,
                },
            )

    def test_cell_already_taken_by_player(self):
        player_x, player_o, season, game = self.create_players_season_game()

        db.session.add(
            TurnModel(player_id=player_x.id, row=0, col=0, game_id=game.id)
        )
        db.session.commit()

        with self.assertRaises(werkzeug.exceptions.Conflict):
            GameService().make_turn(
                game_id=game.id,
                turn={
                    "player_id": player_x.id,
                    "row": 0,
                    "col": 0,
                },
            )

    def test_invalid_turn(self):
        player_x, player_o, season, game = self.create_players_season_game()

        with self.assertRaises(werkzeug.exceptions.BadRequest):
            GameService().make_turn(
                game_id=game.id,
                turn={
                    "player_id": player_x.id,
                    "row": 3,
                    "col": 0,
                },
            )

    def test_player_turn(self):
        player_x, player_o, season, game = self.create_players_season_game()

        resp = GameService().make_turn(
            game_id=game.id,
            turn={
                "player_id": player_x.id,
                "row": 0,
                "col": 0,
            },
        )

        self.assertEquals(
            resp,
            (
                {
                    "col": 0,
                    "player_id": 1,
                    "row": 0,
                },
                200,
            ),
        )
        retrieved_game = GameModel.query.first()
        self.assertEqual(len(retrieved_game.turns), 1)
        self.assertEqual(retrieved_game.winner_id, None)
        self.assertEqual(retrieved_game.current_player_id, player_o.id)

    def test_player_turn_to_win_row(self):
        player_x, player_o, season, game = self.create_players_season_game()
        turns = [
            TurnModel(player_id=player_x.id, row=0, col=0, game_id=game.id),
            TurnModel(player_id=player_o.id, row=1, col=0, game_id=game.id),
            TurnModel(player_id=player_x.id, row=0, col=1, game_id=game.id),
            TurnModel(player_id=player_o.id, row=1, col=1, game_id=game.id),
        ]
        db.session.add_all(turns)
        db.session.commit()

        resp = GameService().make_turn(
            game_id=game.id,
            turn={
                "player_id": player_x.id,
                "row": 0,
                "col": 2,
            },
        )

        self.assertEquals(
            resp,
            (
                {"col": 2, "player_id": 1, "row": 0},
                200,
            ),
        )
        retrieved_game = GameModel.query.first()
        self.assertEqual(retrieved_game.winner_id, player_x.id)
