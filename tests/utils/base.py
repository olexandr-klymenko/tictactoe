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
    def create_players_season_game(
        player_x_name="Test Player 1",
        player_x_email="test1@example.com",
        player_o_name="Test Player 2",
        player_o_email="test2@example.com",
        season_name="Test season 1",
    ):
        player_x = PlayerModel(name=player_x_name, email=player_x_email)
        player_o = PlayerModel(name=player_o_name, email=player_o_email)
        season = SeasonModel(name=season_name)
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
