from app.models import GameModel
from tests.utils.base import BaseTestCase


class TestModels(BaseTestCase):
    def test_game_switch_current_player(self):
        player_x, player_o, season, game = self.create_players_season_game()
        game.switch_current_player()
        retrieved_game = GameModel.query.first()
        self.assertEqual(retrieved_game.current_player_id, player_o.id)
        game.switch_current_player()
        retrieved_game = GameModel.query.first()
        self.assertEqual(retrieved_game.current_player_id, player_x.id)
