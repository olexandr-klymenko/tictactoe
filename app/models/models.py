from sqlalchemy import ForeignKey, Integer

from app import db


class PlayerModel(db.Model):
    __tablename__ = "player"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    country = db.Column(db.String(50), nullable=True)

    turns = db.relationship("GameTurnModel", backref="player", lazy=True)


class GameTurnModel(db.Model):
    __tablename__ = "turn"
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(
        db.Integer, db.ForeignKey("player.id"), nullable=False
    )
    row = db.Column(db.Integer, nullable=False)
    col = db.Column(db.Integer, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)


class GameModel(db.Model):
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
    turns = db.relationship("GameTurnModel", backref="game", lazy=True)

    @property
    def players(self):
        return self.player_x_id, self.player_o_id

    @property
    def status(self):
        if self.winner_id or len(self.turns) == 9:
            return "FINISHED"
        return "IN PROGRESS"

    def switch_current_player(self):
        if self.current_player_id == self.player_x_id:
            self.current_player_id = self.player_o_id
        else:
            self.current_player_id = self.player_x_id

        db.session.commit()

    def __init__(self, player_x_id, player_o_id, season_id):
        self.player_x_id = player_x_id
        self.player_o_id = player_o_id
        self.season_id = season_id
        self.current_player_id = (
            player_x_id  # Set current player to player X by default
        )


class SeasonModel(db.Model):
    __tablename__ = "season"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    games = db.relationship("GameModel", backref="season", lazy=True)

    @classmethod
    def current_season_id(cls):
        return cls.query.order_by(cls.id.desc()).first().id

    def __init__(self, name):
        self.name = name
