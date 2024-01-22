from app.models.schemas import BoardSchema


def load_data(game_db_obj):
    """ Load user's data

    Parameters:
    - Game db object
    """
    board_schema = BoardSchema()

    data = board_schema.dump(game_db_obj)

    return data
