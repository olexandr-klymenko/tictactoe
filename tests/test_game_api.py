import json

from app import db
from app.models.models import TicTacToeGame, Player, TicTacToeTurn

from tests.utils.base import BaseTestCase


class TestGameBlueprint(BaseTestCase):
    def test_start_game(self):
        """Test starting tic-tac-toe game"""
        player_x = Player(name="Test Player 1", email="test1@example.com")
        player_o = Player(name="Test Player 2", email="test2@example.com")
        db.session.add(player_x)
        db.session.add(player_o)
        db.session.commit()
        resp = self.client.post(
            "/api/game/",
            json={
                "player_x_id": player_x.id,
                "player_o_id": player_o.id,
            },
        )
        self.assertEqual(resp.status_code, 201)
        retrieved_game = TicTacToeGame.query.first()
        data = json.loads(resp.data.decode())
        self.assertEqual(retrieved_game.id, data["data"]["game_id"])

    def test_start_game_fail(self):
        """Test starting tic-tac-toe game"""
        player_x = Player(name="Test Player 1", email="test1@example.com")
        db.session.add(player_x)
        db.session.commit()
        resp = self.client.post(
            "/api/game/",
            json={
                "player_x_id": player_x.id,
                "player_o_id": 999,
            },
        )
        self.assertEqual(resp.status_code, 400)

    def test_view_board(self):
        player_x, player_o, game = self.create_players_and_game()
        turns = [
            TicTacToeTurn(
                player_id=player_x.id, row=0, col=0, game_id=game.id
            ),
            TicTacToeTurn(
                player_id=player_o.id, row=0, col=2, game_id=game.id
            ),
            TicTacToeTurn(
                player_id=player_x.id, row=1, col=1, game_id=game.id
            ),
            TicTacToeTurn(
                player_id=player_o.id, row=2, col=0, game_id=game.id
            ),
        ]
        db.session.add_all(turns)
        db.session.commit()
        resp = self.client.get(f"/api/game/{game.id}")
        game_data = json.loads(resp.data.decode())

        self.assertEqual(
            game_data["data"],
            {
                "board": [["X", "_", "O"], ["_", "X", "_"], ["O", "_", "_"]],
                "current_player": "Test Player 1",
                "player_o": "Test Player 2",
                "player_x": "Test Player 1",
                "winner": None,
            },
        )

    def test_make_turn(self):
        player_x, player_o, game = self.create_players_and_game()
        resp = self.client.put(
            f"/api/game/{game.id}",
            json={
                "player_id": player_x.id,
                "row": 0,
                "col": 0,
            },
        )
        self.assertEqual(resp.status_code, 200)
        retrieved_game = TicTacToeGame.query.first()
        self.assertEqual(len(retrieved_game.turns), 1)
