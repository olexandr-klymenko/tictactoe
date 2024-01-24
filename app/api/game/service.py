from sqlalchemy import or_, not_

from app import db
from app.models import (
    GameModel,
    TurnModel,
    SeasonModel,
    PlayerModel,
)
from app.schemas import GameBoardSchema, GameStartSchema, GameStatsSchema
from app.utils import err_resp

from .game_logic_utils import (
    is_cell_already_taken,
    is_valid_turn,
    is_winner,
    is_finished,
)


class GameService:
    @staticmethod
    def start_game(data):
        if data["player_x_id"] == data["player_o_id"]:
            return err_resp(
                "Can't start game with one player", "game_400", 400
            )

        # Make sure player 1 is in the database
        player_x = PlayerModel.query.filter(
            PlayerModel.id == data["player_x_id"]
        ).first()
        if not player_x:
            return err_resp("Player 1 not found!", "player_404", 404)

        # Make sure player 2 is in the database
        player_o = PlayerModel.query.filter(
            PlayerModel.id == data["player_o_id"]
        ).first()
        if not player_o:
            return err_resp("Player 2 not found!", "player_404", 404)

        game = GameModel(
            player_x_id=data["player_x_id"],
            player_o_id=data["player_o_id"],
            season_id=SeasonModel.current_season_id(),
        )
        db.session.add(game)
        db.session.commit()
        return GameStartSchema().dump(game), 201

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
        return GameStatsSchema(many=True).dump(games_query.all()), 200

    @staticmethod
    def view_board(game_id):
        """Get game board data by game_id"""
        if not (game := GameModel.query.filter_by(id=game_id).first()):
            return err_resp("Game not found!", "user_404", 404)

        return GameBoardSchema().dump(game), 200

    @staticmethod
    def make_turn(game_id, turn):
        player_id = turn["player_id"]
        if not (game := GameModel.query.filter_by(id=game_id).first()):
            return err_resp("Game not found!", "game_404", 404)

        if is_finished(game):  # Turn can't be made in the finished game
            return err_resp("Game finished!", "game_409", 409)

        if (
            player_id not in game.players
        ):  # Player doesn't participate in the game
            return err_resp("Player not authorized!", "player_403", 403)

        if (
            player_id != game.current_player_id
        ):  # This is not turn of the player
            return err_resp("Not your turn!", "player_403", 403)

        if is_cell_already_taken(
            turn, game.turns
        ):  # This cell was taken by one of the previous turns
            return err_resp("Cell is already taken!", "turn_409", 409)

        if not is_valid_turn(turn):
            return err_resp("Invalid turn!", "turn_400", 400)

        db.session.add(
            TurnModel(
                player_id=player_id,
                row=turn["row"],
                col=turn["col"],
                game_id=game.id,
            ),
        )
        game.switch_current_player()

        if is_winner(
            game_turns=game.turns, latest_turn=turn
        ):  # Check if the turn wins the game
            game.winner_id = player_id

        db.session.commit()

        return turn, 200
