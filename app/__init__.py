""" Top level module

This module:

- Contains create_app()
- Registers extensions
"""

from flask import Flask

# Import extensions
from .extensions import db, ma

# Import config
from config import config_by_name


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    register_extensions(app)

    # Register blueprints

    from .api import api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    return app


def register_extensions(app):
    # Registers flask extensions
    db.init_app(app)
    ma.init_app(app)

    if "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"]:

        def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
            dbapi_con.execute("pragma foreign_keys=ON")

        with app.app_context():
            from sqlalchemy import event

            event.listen(db.engine, "connect", _fk_pragma_on_connect)
