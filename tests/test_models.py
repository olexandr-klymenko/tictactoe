import sqlalchemy

from app import db
from app.models.models import Player, TicTacToeGame, TicTacToeMove

from tests.utils.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_create_player(self):
        # Create a test player
        player = Player(name="John Doe", age=25, email="john@example.com", country="USA")
        db.session.add(player)
        db.session.commit()

        # Retrieve the player from the database
        retrieved_player = Player.query.filter_by(name="John Doe").first()

        # Assert that the retrieved player matches the created player
        assert retrieved_player is not None
        assert retrieved_player.name == "John Doe"
        assert retrieved_player.age == 25
        assert retrieved_player.email == "john@example.com"
        assert retrieved_player.country == "USA"

    def test_create_tic_tac_toe_game(self):
        # Create test players
        player_x = Player(name="Player X", email="player_x@example.com")
        player_o = Player(name="Player O", email="player_o@example.com")
        db.session.add_all([player_x, player_o])
        db.session.commit()

        # Create a test TicTacToeGame
        game = TicTacToeGame(player_X_id=player_x.id, player_O_id=player_o.id)
        db.session.add(game)
        db.session.commit()

        # Retrieve the game from the database
        retrieved_game = TicTacToeGame.query.first()

        # Assert that the retrieved game matches the created game
        assert retrieved_game is not None
        assert retrieved_game.player_X_id == player_x.id
        assert retrieved_game.player_O_id == player_o.id
        assert retrieved_game.current_player_id == player_x.id

    def test_create_tic_tac_toe_move(self):
        # Create a test player
        player = Player(name="Test Player", email="test@example.com")
        db.session.add(player)
        db.session.commit()

        # Create a test TicTacToeGame
        game = TicTacToeGame(player_X_id=player.id, player_O_id=player.id)
        db.session.add(game)
        db.session.commit()

        # Create a test TicTacToeMove
        move = TicTacToeMove(player_id=player.id, row=1, col=1, game_id=game.id)
        db.session.add(move)
        db.session.commit()

        # Retrieve the move from the database
        retrieved_move = TicTacToeMove.query.first()

        # Assert that the retrieved move matches the created move
        assert retrieved_move is not None
        assert retrieved_move.player_id == player.id
        assert retrieved_move.row == 1
        assert retrieved_move.col == 1
        assert retrieved_move.game_id == game.id

        retrieved_game = TicTacToeGame.query.first()
        self.assertEqual(len(retrieved_game.moves), 1)
        retrieved_player = Player.query.first()
        self.assertEqual(len(retrieved_player.moves), 1)
