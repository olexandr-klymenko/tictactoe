from sqlalchemy import ForeignKey, Integer

from app import db


class PlayerModel(db.Model):
    __tablename__ = "player"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    country = db.Column(db.String(50), nullable=True)

    turns = db.relationship("TurnModel", backref="player", lazy=True)


class TurnModel(db.Model):
    __tablename__ = "turn"
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(
        db.Integer, db.ForeignKey("player.id"), nullable=False
    )
    row = db.Column(db.Integer, nullable=False)
    col = db.Column(db.Integer, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)


class GameModel(db.Model):
    """Game model"""

    __tablename__ = "game"
    id = db.Column(Integer, primary_key=True)
    player_x_id = db.Column(Integer, ForeignKey("player.id"), nullable=False)
    player_o_id = db.Column(Integer, ForeignKey("player.id"), nullable=False)
    current_player_id = db.Column(
        Integer, ForeignKey("player.id"), nullable=False
    )
    winner_id = db.Column(db.Integer, db.ForeignKey("player.id"), default=None)
    season_id = db.Column(
        db.Integer, db.ForeignKey("season.id"), nullable=False
    )

    player_x = db.relationship("PlayerModel", foreign_keys=[player_x_id])
    player_o = db.relationship("PlayerModel", foreign_keys=[player_o_id])
    winner = db.relationship("PlayerModel", foreign_keys=[winner_id])

    current_player = db.relationship(
        "PlayerModel", foreign_keys=[current_player_id]
    )
    turns = db.relationship("TurnModel", backref="game", lazy=True)

    @property
    def players(self):
        return self.player_x_id, self.player_o_id

    def switch_current_player(self):
        """Switch current player after making turn"""
        if self.current_player_id == self.player_x_id:
            self.current_player_id = self.player_o_id
        else:
            self.current_player_id = self.player_x_id

        db.session.commit()

    def __init__(self, player_x_id, player_o_id, season_id):
        """Takes ids of the first and the second players and the season_id"""
        self.player_x_id = player_x_id
        self.player_o_id = player_o_id
        self.season_id = season_id  # current season id
        self.current_player_id = (
            player_x_id  # Set current player to player X by default
        )


class SeasonModel(db.Model):
    """League season model"""

    __tablename__ = "season"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    games = db.relationship("GameModel", backref="season", lazy=True)

    @classmethod
    def current_season_id(cls):
        """
        Assuming that primary key is integer and autoincrement.
        Therefore, the current season is the biggest one.
        """
        return cls.query.order_by(cls.id.desc()).first().id

    def __init__(self, name):
        self.name = name
