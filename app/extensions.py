"""
Extensions module

Each extension is initialized when app is created.
"""

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()

migrate = Migrate()
ma = Marshmallow()
