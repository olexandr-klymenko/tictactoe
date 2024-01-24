from typing import Iterable

from app.models import TurnModel

GAME_BOARD_SIZE = 3


def is_cell_already_taken(turn, game_turns: Iterable["TurnModel"]):
    # Extract the row and column from the provided turn
    # Check if the specified cell coordinates match any of the previous turns
    for previous_turn in [{"row": t.row, "col": t.col} for t in game_turns]:
        if (
            previous_turn["row"] == turn["row"]
            and previous_turn["col"] == turn["col"]
        ):
            return True  # The cell is already taken

    return False  # The cell is not taken


def is_winner(game_turns: Iterable["TurnModel"], latest_turn):
    """
    Check is winner condition
    We assume that board size is 3.
    Otherwise, the is_winner logic would be much more complex.
    """
    player_turns = {
        (t.row, t.col)
        for t in game_turns
        if t.player_id == latest_turn["player_id"]
    }
    if len(player_turns) < 3:  # Not enough turns to win the game
        return False

    # check vertical line
    if (
        len([row for row, col in player_turns if row == latest_turn["row"]])
        == GAME_BOARD_SIZE
    ):
        return True

    # check horizontal line
    if (
        len([col for row, col in player_turns if col == latest_turn["col"]])
        == GAME_BOARD_SIZE
    ):
        return True

    # check diagonal lines
    if len({(0, 0), (1, 1), (2, 2)}.intersection(player_turns)) == 3:
        return True

    if len({(2, 0), (1, 1), (0, 2)}.intersection(player_turns)) == 3:
        return True

    return False


def is_valid_turn(turn):
    """Check if turn cell is within the board"""
    if (
        0 < turn["row"] > GAME_BOARD_SIZE - 1
        or 0 < turn["col"] > GAME_BOARD_SIZE - 1
    ):
        return False
    return True
