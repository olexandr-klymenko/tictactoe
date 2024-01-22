# Model Schemas
from marshmallow import fields

from app import ma


class BoardSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("player_x", "player_o", "current_player", "winner", "board")

    player_x = fields.Function(lambda obj: obj.player_x.name)
    player_o = fields.Function(lambda obj: obj.player_o.name)
    current_player = fields.Function(lambda obj: obj.current_player.name)
    winner = fields.Function(lambda obj: obj.winner.name if obj.winner else None)

    # Serialize the board as a 2D matrix
    board = fields.Method("get_board")

    def get_board(self, obj):
        board = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]
        for move in obj.turns:
            if move.player_id == obj.player_x.id:
                board[move.row][move.col] = "X"
            else:
                board[move.row][move.col] = "O"
        return board


class GameStartSchema(ma.Schema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("game_id",)

    game_id = fields.Function(lambda obj: obj.id)
