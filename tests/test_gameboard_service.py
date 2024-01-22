from app import db
from app.models.models import Player, TicTacToeGame, TicTacToeTurn
from app.api.game.service import GameService

from tests.utils.base import BaseTestCase


class TestGameService(BaseTestCase):
    def test_view_board(self):
        player_x, player_o, game = self.create_players_and_game()

        turns = [
            TicTacToeTurn(
                player_id=player_x.id, row=0, col=0, game_id=game.id
            ),
            TicTacToeTurn(
                player_id=player_o.id, row=1, col=1, game_id=game.id
            ),
            TicTacToeTurn(
                player_id=player_x.id, row=0, col=1, game_id=game.id
            ),
            TicTacToeTurn(
                player_id=player_o.id, row=0, col=2, game_id=game.id
            ),
            TicTacToeTurn(
                player_id=player_x.id, row=1, col=0, game_id=game.id
            ),
            TicTacToeTurn(
                player_id=player_o.id, row=2, col=0, game_id=game.id
            ),
        ]
        db.session.add_all(turns)
        db.session.commit()
        resp = GameService.view_board(game.id)
        self.assertEquals(
            resp[0]["data"],
            {
                "player_x": "Test Player 1",
                "player_o": "Test Player 2",
                "current_player": "Test Player 1",
                "winner": None,
                "board": [["X", "X", "O"], ["X", "O", "_"], ["O", "_", "_"]],
            },
        )

    def test_make_turn_game_not_found(self):
        resp = GameService().make_turn(
            game_id=999,
            turn={
                "player_id": 1,
                "row": 0,
                "col": 0,
            },
        )
        self.assertEquals(
            resp,
            (
                {
                    "status": False,
                    "message": "Game not found!",
                    "error_reason": "game_404",
                },
                404,
            ),
        )

    def test_make_turn_game_finished(self):
        player_x, player_o, game = self.create_players_and_game()
        game.winner_id = player_x.id
        db.session.add(game)
        db.session.commit()

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
                    "status": False,
                    "message": "Game finished!",
                    "error_reason": "game_409",
                },
                409,
            ),
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

        resp = GameService().make_turn(
            game_id=game.id,
            turn={
                "player_id": player_i.id,
                "row": 0,
                "col": 0,
            },
        )
        self.assertEquals(
            resp,
            (
                {
                    "status": False,
                    "message": "Player not authorized!",
                    "error_reason": "player_403",
                },
                403,
            ),
        )

    def test_make_turn_not_current_player(self):
        player_x, player_o, game = self.create_players_and_game()

        resp = GameService().make_turn(
            game_id=game.id,
            turn={
                "player_id": player_o.id,
                "row": 0,
                "col": 0,
            },
        )
        self.assertEquals(
            resp,
            (
                {
                    "status": False,
                    "message": "Not your turn!",
                    "error_reason": "player_403",
                },
                403,
            ),
        )

    def test_cell_already_taken_by_player(self):
        player_x, player_o, game = self.create_players_and_game()

        db.session.add(
            TicTacToeTurn(player_id=player_x.id, row=0, col=0, game_id=game.id)
        )
        db.session.commit()

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
                    "status": False,
                    "message": "Cell is already taken!",
                    "error_reason": "turn_409",
                },
                409,
            ),
        )

    def test_invalid_turn(self):
        player_x, player_o, game = self.create_players_and_game()

        resp = GameService().make_turn(
            game_id=game.id,
            turn={
                "player_id": player_x.id,
                "row": 3,
                "col": 0,
            },
        )

        self.assertEquals(
            resp,
            (
                {
                    "status": False,
                    "message": "Invalid turn!",
                    "error_reason": "turn_400",
                },
                400,
            ),
        )

    def test_player_turn(self):
        player_x, player_o, game = self.create_players_and_game()

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
                    "message": "Turn has been made",
                    "status": True,
                    "data": {"col": 0, "player_id": 1, "row": 0},
                },
                200,
            ),
        )
        retrieved_game = TicTacToeGame.query.first()
        self.assertEqual(len(retrieved_game.turns), 1)
        self.assertEqual(retrieved_game.winner_id, None)
        self.assertEqual(retrieved_game.current_player_id, player_o.id)

    def test_player_turn_to_win_row(self):
        player_x, player_o, game = self.create_players_and_game()
        turns = [
            TicTacToeTurn(
                player_id=player_x.id, row=0, col=0, game_id=game.id
            ),
            TicTacToeTurn(
                player_id=player_o.id, row=1, col=0, game_id=game.id
            ),
            TicTacToeTurn(
                player_id=player_x.id, row=0, col=1, game_id=game.id
            ),
            TicTacToeTurn(
                player_id=player_o.id, row=1, col=1, game_id=game.id
            ),
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
                {
                    "message": "Turn has been made",
                    "status": True,
                    "data": {"col": 2, "player_id": 1, "row": 0},
                },
                200,
            ),
        )
        retrieved_game = TicTacToeGame.query.first()
        self.assertEqual(retrieved_game.winner_id, player_x.id)

    def test_player_turn_to_win_col(self):
        player_x, player_o, game = self.create_players_and_game()
        turns = [
            TicTacToeTurn(
                player_id=player_x.id, row=0, col=0, game_id=game.id
            ),
            TicTacToeTurn(
                player_id=player_o.id, row=0, col=1, game_id=game.id
            ),
            TicTacToeTurn(
                player_id=player_x.id, row=1, col=0, game_id=game.id
            ),
            TicTacToeTurn(
                player_id=player_o.id, row=1, col=1, game_id=game.id
            ),
        ]
        db.session.add_all(turns)
        db.session.commit()

        resp = GameService().make_turn(
            game_id=game.id,
            turn={
                "player_id": player_x.id,
                "row": 2,
                "col": 0,
            },
        )

        self.assertEquals(
            resp,
            (
                {
                    "message": "Turn has been made",
                    "status": True,
                    "data": {"col": 0, "player_id": 1, "row": 2},
                },
                200,
            ),
        )
        retrieved_game = TicTacToeGame.query.first()
        self.assertEqual(retrieved_game.winner_id, player_x.id)

    def test_player_turn_to_win_diagonal(self):
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

        resp = GameService().make_turn(
            game_id=game.id,
            turn={
                "player_id": player_x.id,
                "row": 2,
                "col": 2,
            },
        )

        self.assertEquals(
            resp,
            (
                {
                    "message": "Turn has been made",
                    "status": True,
                    "data": {"col": 2, "player_id": 1, "row": 2},
                },
                200,
            ),
        )
        retrieved_game = TicTacToeGame.query.first()
        self.assertEqual(retrieved_game.winner_id, player_x.id)
