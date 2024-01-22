GAME_BOARD_SIZE = 3


def is_cell_already_taken(turn, game_turns):
    # Extract the row and column from the provided turn
    # Check if the specified cell coordinates match any of the previous turns
    for previous_turn in [{"row": t.row, "col": t.col} for t in game_turns]:
        if (
            previous_turn["row"] == turn["row"]
            and previous_turn["col"] == turn["col"]
        ):
            return True  # The cell is already taken

    return False  # The cell is not taken


def is_winner(game_turns, turn):
    player_turns = [
        {"row": t.row, "col": t.col}
        for t in game_turns
        if t.player_id == turn["player_id"]
    ]
    if len(player_turns) < 3:  # Not enough turns to win
        return False

    row = turn["row"]
    col = turn["col"]

    # row line
    if len([t for t in player_turns if t["row"] == row]) == GAME_BOARD_SIZE:
        return True

    # col line
    if len([t for t in player_turns if t["col"] == col]) == GAME_BOARD_SIZE:
        return True

    # diagonal lines
    if row + col % 2 == 1:  # turn cell not in any of the corners
        return False

    if {
        "row": 1,
        "col": 1,
    } in player_turns:  # diagonal should contain center cell
        return True

    return False


def is_valid_turn(turn):
    if (
        0 < turn["row"] > GAME_BOARD_SIZE - 1
        or 0 < turn["col"] > GAME_BOARD_SIZE - 1
    ):
        return False
    return True
