import unittest

from app import create_app, db
from app.models.models import GameModel, PlayerModel, SeasonModel


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        db.create_all()

    @staticmethod
    def create_players_season_game():
        player_x = PlayerModel(name="Test Player 1", email="test1@example.com")
        player_o = PlayerModel(name="Test Player 2", email="test2@example.com")
        season = SeasonModel(name="Test season")
        db.session.add_all([player_x, player_o, season])
        db.session.commit()

        game = GameModel(
            player_x_id=player_x.id,
            player_o_id=player_o.id,
            season_id=season.id,
        )
        db.session.add(game)
        db.session.commit()
        return player_x, player_o, season, game

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
