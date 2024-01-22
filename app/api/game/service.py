from flask import current_app

from app import db
from app.utils import err_resp, message, internal_err_resp
from .utils import is_cell_already_taken, is_winner
from app.models.models import TicTacToeGame, TicTacToeTurn
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
            return err_resp("Not your turn!", "player_403", 403)

        if is_cell_already_taken(turn, game.turns):
            return err_resp("Cell is already taken!", "turn_409", 409)

        if 0 < turn["row"] > 2 or 0 < turn["col"] > 2:
            return err_resp("Invalid turn!", "turn_400", 400)

        db.session.add(
            TicTacToeTurn(
                player_id=player_id,
                row=turn["row"],
                col=turn["col"],
                game_id=game.id,
            ),
        )
        game.switch_current_player()
        db.session.commit()

        if is_winner(game_turns=game.turns, turn=turn):
            game.winner_id = player_id
            db.session.commit()

        return message(status=True, message="Turn has been made"), 201

    @staticmethod
    def view_board(game_id):
        """Get game board data by game_id"""
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
