import sqlalchemy
from flask import current_app
from sqlalchemy import and_, case, func, or_, not_

from app import db
from app.models.models import GameModel, GameTurnModel, SeasonModel
from app.models.schemas import BoardSchema, GameStartSchema, GameSchema
from app.utils import err_resp, internal_err_resp

from .utils import is_cell_already_taken, is_valid_turn, is_winner


class GameService:
    @staticmethod
    def start_game(data):
        try:
            game = GameModel(
                player_x_id=data["player_x_id"],
                player_o_id=data["player_o_id"],
                season_id=SeasonModel.current_season_id(),
            )
            db.session.add(game)
            db.session.commit()
            return GameStartSchema().dump(game), 201

        except sqlalchemy.exc.IntegrityError as error:
            db.session.rollback()
            current_app.logger.error(error)
            return err_resp("An integrity error occurred!", "game_400", 400)

        except Exception as error:
            db.session.rollback()
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def list_games(season_id=None, player_id=None, is_draw=None):
        games_query = db.session.query(GameModel)
        if season_id:
            games_query = games_query.filter(GameModel.season_id == season_id)
        if player_id:
            games_query = games_query.filter(
                or_(
                    GameModel.player_x_id == player_id,
                    GameModel.player_o_id == player_id,
                )
            )
        if is_draw is True:
            games_query = games_query.filter(GameModel.winner_id.is_(None))
        elif is_draw is False:
            games_query = games_query.filter(
                not_(GameModel.winner_id.is_(None))
            )
        return [GameSchema().dump(game) for game in games_query.all()], 200

    @staticmethod
    def view_board(game_id):
        """Get game board data by game_id"""
        if not (game := GameModel.query.filter_by(id=game_id).first()):
            return err_resp("Game not found!", "user_404", 404)

        try:
            return BoardSchema().dump(game), 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def make_turn(game_id, turn):
        player_id = turn["player_id"]
        if not (game := GameModel.query.filter_by(id=game_id).first()):
            return err_resp("Game not found!", "game_404", 404)

        if game.is_finished:
            return err_resp("Game finished!", "game_409", 409)

        if player_id not in game.players:
            return err_resp("Player not authorized!", "player_403", 403)

        if player_id != game.current_player_id:
            return err_resp("Not your turn!", "player_403", 403)

        if is_cell_already_taken(turn, game.turns):
            return err_resp("Cell is already taken!", "turn_409", 409)

        if not is_valid_turn(turn):
            return err_resp("Invalid turn!", "turn_400", 400)

        db.session.add(
            GameTurnModel(
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

        return turn, 200
