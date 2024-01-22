"""
Extensions module

Each extension is initialized when app is created.
"""

from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

migrate = Migrate()
ma = Marshmallow()
