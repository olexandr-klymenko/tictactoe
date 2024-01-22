from app import db
from app.models.models import Player, TicTacToeGame, TicTacToeTurn
from app.api.game.service import GameBoardService
from app.api.game.dto import TurnDto

from tests.utils.base import BaseTestCase


class TestGameBoardService(BaseTestCase):

    def test_view_board(self):
        player_x = Player(name="Test Player 1", email="test1@example.com")
        player_o = Player(name="Test Player 2", email="test2@example.com")
        db.session.add(player_x)
        db.session.add(player_o)
        db.session.commit()

        game = TicTacToeGame(player_x_id=player_x.id, player_o_id=player_o.id)
        db.session.add(game)
        db.session.commit()

        moves = [
            TicTacToeTurn(player_id=player_x.id, row=1, col=1, game_id=game.id),
            TicTacToeTurn(player_id=player_o.id, row=2, col=2, game_id=game.id),
            TicTacToeTurn(player_id=player_x.id, row=1, col=2, game_id=game.id),
            TicTacToeTurn(player_id=player_o.id, row=1, col=3, game_id=game.id),
            TicTacToeTurn(player_id=player_x.id, row=2, col=1, game_id=game.id),
            TicTacToeTurn(player_id=player_o.id, row=3, col=1, game_id=game.id),
        ]
        db.session.add_all(moves)
        db.session.commit()
        resp = GameBoardService.view_board(game.id)
        self.assertEquals(
            resp[0]["game"],
            {
                'player_x': 'Test Player 1',
                'player_o': 'Test Player 2',
                'current_player': 'Test Player 1',
                'board': [['X', 'X', 'O'], ['X', 'O', '_'], ['O', '_', '_']]
            }
        )

    def test_make_turn_game_not_found(self):
        resp = GameBoardService().make_turn(
            {
                "game_id": 1,
                "player_id": 1,
                "row": 0,
                "col": 0,
            }
        )
        self.assertEquals(
            resp, ({
                       "status": False,
                       "message": "Game not found!",
                       "error_reason": "game_404",
                   }, 404)
        )

    def test_make_turn_game_finished(self):
        player_x = Player(name="Test Player 1", email="test1@example.com")
        player_o = Player(name="Test Player 2", email="test2@example.com")
        db.session.add_all([player_x, player_o])
        db.session.commit()

        game = TicTacToeGame(player_x_id=player_x.id, player_o_id=player_o.id)
        game.winner_id = player_x.id
        db.session.add(game)
        db.session.commit()

        resp = GameBoardService().make_turn(
            {
                "game_id": game.id,
                "player_id": player_x.id,
                "row": 0,
                "col": 0,
            }
        )
        self.assertEquals(
            resp, ({
                       "status": False,
                       "message": "Game finished!",
                       "error_reason": "game_409",
                   }, 409)
        )

    def test_make_turn_not_authorized(self):
        player_x = Player(name="Test Player 1", email="test1@example.com")
        player_o = Player(name="Test Player 2", email="test2@example.com")
        player_i = Player(name="Test Player 3", email="test3@example.com")
        db.session.add_all([player_x, player_o, player_i])
        db.session.commit()

        game = TicTacToeGame(player_x_id=player_x.id, player_o_id=player_o.id)
        db.session.add(game)
        db.session.commit()

        resp = GameBoardService().make_turn(
            {
                "game_id": game.id,
                "player_id": player_i.id,
                "row": 0,
                "col": 0,
            }
        )
        self.assertEquals(
            resp, ({
                       "status": False,
                       "message": "Player not authorized!",
                       "error_reason": "player_403",
                   }, 403)
        )

    def test_make_turn_not_current_player(self):
        player_x = Player(name="Test Player 1", email="test1@example.com")
        player_o = Player(name="Test Player 2", email="test2@example.com")
        db.session.add_all([player_x, player_o])
        db.session.commit()

        game = TicTacToeGame(player_x_id=player_x.id, player_o_id=player_o.id)
        db.session.add(game)
        db.session.commit()

        resp = GameBoardService().make_turn(
            {
                "game_id": game.id,
                "player_id": player_o.id,
                "row": 0,
                "col": 0,
            }
        )
        self.assertEquals(
            resp, ({
                       "status": False,
                       "message": "Not Your Turn!",
                       "error_reason": "player_403",
                   }, 403)
        )
