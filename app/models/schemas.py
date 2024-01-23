# Model Schemas
from marshmallow import fields

from app import ma


class BoardSchema(ma.Schema):
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
        board = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]
        for turn in obj.turns:
            if turn.player_id == obj.player_x.id:
                board[turn.row][turn.col] = "X"
            else:
                board[turn.row][turn.col] = "O"
        return board


class GameStartSchema(ma.Schema):
    class Meta:
        fields = ("game_id",)

    game_id = fields.Function(lambda obj: obj.id)


class RankingRecordSchema(ma.Schema):
    class Meta:
        fields = ("rank", "player_id", "player_name", "total_points")

    rank = fields.Function(lambda obj: obj["rank"])
    player_id = fields.Function(lambda obj: obj["player_id"])
    player_name = fields.Function(lambda obj: obj["player_name"])
    total_points = fields.Function(lambda obj: obj["total_points"])
