from marshmallow import fields

from .models import PlayerModel
from app import ma


class GameStartSchema(ma.Schema):
    class Meta:
        fields = ("game_id",)

    game_id = fields.Function(lambda obj: obj.id)


class GameSchema(ma.Schema):
    class Meta:
        fields = (
            "season_id",
            "game_id",
            "player_x",
            "player_o",
            "winner",
            "turns",
        )

    season_id = fields.Function(lambda obj: obj.season_id)
    game_id = fields.Function(lambda obj: obj.id)
    player_x = fields.Function(lambda obj: obj.player_x.name)
    player_o = fields.Function(lambda obj: obj.player_o.name)
    winner = fields.Function(
        lambda obj: obj.winner.name if obj.winner else None
    )
    turns = fields.Function(lambda obj: len(obj.turns))


class BoardSchema(ma.Schema):
    """The schema for game model into readable board details"""

    class Meta:
        fields = ("player_x", "player_o", "current_player", "winner", "board")

    player_x = fields.Function(lambda obj: obj.player_x.name)
    player_o = fields.Function(lambda obj: obj.player_o.name)
    current_player = fields.Function(lambda obj: obj.current_player.name)
    winner = fields.Function(
        lambda obj: obj.winner.name if obj.winner else None
    )

    # Serialize the board as a 2D matrix
    board = fields.Method("get_board")

    @staticmethod
    def get_board(obj):
        """
        Render game board.
        '_': empty cell
        'X': cell taken by the first player
        'O': cell taken by the second player
        """
        board = [
            ["_", "_", "_"],
            ["_", "_", "_"],
            ["_", "_", "_"],
        ]  # fill board with empty cells
        for turn in obj.turns:
            if turn.player_id == obj.player_x.id:
                board[turn.row][turn.col] = "X"
            else:
                board[turn.row][turn.col] = "O"
        return board


class RankingRecordSchema(ma.Schema):
    class Meta:
        fields = ("rank", "player_id", "player_name", "total_points")

    rank = fields.Function(lambda obj: obj["rank"])
    player_id = fields.Function(lambda obj: obj["player_id"])
    player_name = fields.Function(lambda obj: obj["player_name"])
    total_points = fields.Function(lambda obj: obj["total_points"])


class PlayerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PlayerModel

    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    age = ma.auto_field()
    country = ma.auto_field()


class ListPlayersSchema(ma.Schema):
    class Meta:
        fields = ("name", "links")

    name = fields.Function(lambda obj: obj.name)

    links = ma.Hyperlinks(
        {
            "self": ma.URLFor("api.admin_player", values=dict(id="<id>")),
            "collection": ma.URLFor("api.admin_players"),
        }
    )
