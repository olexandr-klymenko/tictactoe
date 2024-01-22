from flask import current_app

from app.utils import err_resp, message, internal_err_resp
from app.models.models import TicTacToeGame
from app.models.schemas import BoardSchema


class GameBoardService:
    def make_turn(self, turn):
        game_id = turn["game_id"]
        player_id = turn["player_id"]
        if not (game := TicTacToeGame.query.filter_by(id=game_id).first()):
            return err_resp("Game not found!", "game_404", 404)

        if game.status == "FINISHED":
            return err_resp("Game finished!", "game_409", 409)

        if player_id not in game.players:
            return err_resp("Player not authorized!", "player_403", 403)

        if player_id != game.current_player_id:
            return err_resp("Not Your Turn!", "player_403", 403)

        return turn, 201

    @staticmethod
    def view_board(game_id):
        """ Get game board data by game_id """
        if not (game := TicTacToeGame.query.filter_by(id=game_id).first()):
            return err_resp("Game not found!", "user_404", 404)

        try:
            board_schema = BoardSchema()
            board_data = board_schema.dump(game)
            resp = message(True, "Game data sent")
            resp["game"] = board_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
