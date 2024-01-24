from typing import Tuple, Iterable

from app.api.game.game_logic_utils import is_winner, is_finished
from app import db
from app.models import TurnModel

from tests.utils.base import BaseTestCase


class TestIsWinnerConditions(BaseTestCase):
    """Test is winner conditions"""

    def add_turns(self, coordinates: Iterable[Tuple[int, int]]):
        player, _, __, game = self.create_players_season_game()
        turns = [
            TurnModel(player_id=player.id, row=x, col=y, game_id=game.id)
            for x, y in coordinates
        ]
        db.session.add_all(turns)
        db.session.commit()
        return turns

    def test_diagonal_lines_from_top_left(self):
        turns = self.add_turns({(0, 0), (1, 1), (2, 2), (1, 0)})

        self.assertTrue(
            is_winner(
                game_turns=turns,
                latest_turn={"row": 0, "col": 0, "player_id": 1},
            )
        )

    def test_diagonal_lines_from_bottom_left(self):
        turns = self.add_turns({(2, 0), (1, 1), (0, 2), (0, 1)})

        self.assertTrue(
            is_winner(
                game_turns=turns,
                latest_turn={"row": 1, "col": 1, "player_id": 1},
            )
        )

    def test_horizontal_line_true(self):
        turns = self.add_turns({(0, 0), (0, 1), (0, 2), (1, 1)})

        self.assertTrue(
            is_winner(
                game_turns=turns,
                latest_turn={"row": 0, "col": 1, "player_id": 1},
            )
        )

    def test_vertical_line_true(self):
        turns = self.add_turns({(0, 0), (1, 0), (2, 0), (1, 1)})

        self.assertTrue(
            is_winner(
                game_turns=turns,
                latest_turn={"row": 1, "col": 0, "player_id": 1},
            )
        )

    def test_false(self):
        turns = self.add_turns({(0, 0), (1, 1), (2, 0), (1, 2)})

        self.assertFalse(
            is_winner(
                game_turns=turns,
                latest_turn={"row": 2, "col": 0, "player_id": 1},
            )
        )


class TestIsGameFinished(BaseTestCase):
    """Test if game is finished conditions"""

    def test_game_finished_no_empty_cells(self):
        player_x, player_o, season, game = self.create_players_season_game()
        turns = [
            TurnModel(player_id=player_x.id, row=0, col=0, game_id=game.id),
            TurnModel(player_id=player_o.id, row=0, col=1, game_id=game.id),
            TurnModel(player_id=player_x.id, row=0, col=2, game_id=game.id),
            TurnModel(player_id=player_o.id, row=1, col=0, game_id=game.id),
            TurnModel(player_id=player_x.id, row=1, col=1, game_id=game.id),
            TurnModel(player_id=player_o.id, row=1, col=2, game_id=game.id),
            TurnModel(player_id=player_x.id, row=2, col=0, game_id=game.id),
            TurnModel(player_id=player_o.id, row=2, col=1, game_id=game.id),
            TurnModel(player_id=player_x.id, row=2, col=2, game_id=game.id),
        ]
        db.session.add_all(turns)
        db.session.commit()

        self.assertTrue(is_finished(game))

    def test_game_finished_winner(self):
        player_x, player_o, season, game = self.create_players_season_game()
        game.winner_id = player_o.id
        db.session.commit()
        self.assertTrue(is_finished(game))

    def test_game_in_progress(self):
        player_x, player_o, season, game = self.create_players_season_game()
        turns = [
            TurnModel(player_id=player_x.id, row=0, col=0, game_id=game.id),
            TurnModel(player_id=player_o.id, row=0, col=1, game_id=game.id),
            TurnModel(player_id=player_x.id, row=0, col=2, game_id=game.id),
            TurnModel(player_id=player_o.id, row=1, col=0, game_id=game.id),
            TurnModel(player_id=player_x.id, row=1, col=1, game_id=game.id),
        ]
        db.session.add_all(turns)
        db.session.commit()

        self.assertFalse(is_finished(game))
