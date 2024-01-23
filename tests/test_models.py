from app import db
from app.models.models import GameModel, GameTurnModel
from tests.utils.base import BaseTestCase


class TestModels(BaseTestCase):
    def test_game_finished_no_empty_cells(self):
        player_x, player_o, season, game = self.create_players_season_game()
        turns = [
            GameTurnModel(
                player_id=player_x.id, row=0, col=0, game_id=game.id
            ),
            GameTurnModel(
                player_id=player_o.id, row=0, col=1, game_id=game.id
            ),
            GameTurnModel(
                player_id=player_x.id, row=0, col=2, game_id=game.id
            ),
            GameTurnModel(
                player_id=player_o.id, row=1, col=0, game_id=game.id
            ),
            GameTurnModel(
                player_id=player_x.id, row=1, col=1, game_id=game.id
            ),
            GameTurnModel(
                player_id=player_o.id, row=1, col=2, game_id=game.id
            ),
            GameTurnModel(
                player_id=player_x.id, row=2, col=0, game_id=game.id
            ),
            GameTurnModel(
                player_id=player_o.id, row=2, col=1, game_id=game.id
            ),
            GameTurnModel(
                player_id=player_x.id, row=2, col=2, game_id=game.id
            ),
        ]
        db.session.add_all(turns)
        db.session.commit()

        self.assertTrue(game.is_finished)

    def test_game_finished_winner(self):
        player_x, player_o, season, game = self.create_players_season_game()
        game.winner_id = player_o.id
        db.session.commit()
        self.assertTrue(game.is_finished)

    def test_game_in_progress(self):
        player_x, player_o, season, game = self.create_players_season_game()
        turns = [
            GameTurnModel(
                player_id=player_x.id, row=0, col=0, game_id=game.id
            ),
            GameTurnModel(
                player_id=player_o.id, row=0, col=1, game_id=game.id
            ),
            GameTurnModel(
                player_id=player_x.id, row=0, col=2, game_id=game.id
            ),
            GameTurnModel(
                player_id=player_o.id, row=1, col=0, game_id=game.id
            ),
            GameTurnModel(
                player_id=player_x.id, row=1, col=1, game_id=game.id
            ),
        ]
        db.session.add_all(turns)
        db.session.commit()

        self.assertFalse(game.is_finished)

    def test_game_switch_current_player(self):
        player_x, player_o, season, game = self.create_players_season_game()
        game.switch_current_player()
        retrieved_game = GameModel.query.first()
        self.assertEqual(retrieved_game.current_player_id, player_o.id)
        game.switch_current_player()
        retrieved_game = GameModel.query.first()
        self.assertEqual(retrieved_game.current_player_id, player_x.id)
