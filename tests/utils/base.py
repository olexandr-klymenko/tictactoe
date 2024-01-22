import unittest
from app import db, create_app

from app.models.models import Player, TicTacToeGame


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        db.create_all()

    @staticmethod
    def create_players_and_game():
        player_x = Player(name="Test Player 1", email="test1@example.com")
        player_o = Player(name="Test Player 2", email="test2@example.com")
        db.session.add(player_x)
        db.session.add(player_o)
        db.session.commit()

        game = TicTacToeGame(player_x_id=player_x.id, player_o_id=player_o.id)
        db.session.add(game)
        db.session.commit()
        return player_x, player_o, game

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
