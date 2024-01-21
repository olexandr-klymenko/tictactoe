from sqlalchemy import Integer, ForeignKey, DefaultClause, CheckConstraint

from app import db


class Player(db.Model):
    __tablename__ = "player"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    country = db.Column(db.String(50), nullable=True)

    moves = db.relationship('TicTacToeMove', backref='player', lazy=True)


class TicTacToeMove(db.Model):
    __tablename__ = "move"
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    row = db.Column(db.Integer, nullable=False)
    col = db.Column(db.Integer, nullable=False)
    game_id = db.Column(
        db.Integer, db.ForeignKey("game.id"), nullable=False
    )


class TicTacToeGame(db.Model):
    __tablename__ = "game"
    id = db.Column(Integer, primary_key=True)
    player_X_id = db.Column(Integer, ForeignKey('player.id'), nullable=False)
    player_O_id = db.Column(Integer, ForeignKey('player.id'), nullable=False)
    current_player_id = db.Column(Integer, ForeignKey('player.id'), nullable=False)

    player_X = db.relationship("Player", foreign_keys=[player_X_id])
    player_O = db.relationship("Player", foreign_keys=[player_O_id])
    current_player = db.relationship("Player", foreign_keys=[current_player_id])
    moves = db.relationship('TicTacToeMove', backref='game', lazy=True)

    def __init__(self, player_X_id, player_O_id):
        self.player_X_id = player_X_id
        self.player_O_id = player_O_id
        self.current_player_id = player_X_id  # Set current player to player X by default
