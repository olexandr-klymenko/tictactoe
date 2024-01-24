""" Top level module

This module:

- Contains create_app()
- Registers extensions
"""

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

# Import config
from config import config_by_name

# Import extensions
from .extensions import db, ma


def create_app(config_name):
    app = Flask(__name__)

    # By applying ProxyFix to your Flask app,
    # you ensure that it correctly handles requests
    # forwarded by a reverse proxy and interprets headers
    # like X-Forwarded-For, X-Forwarded-Proto,
    # and X-Forwarded-Host when processing requests.
    # This is especially important for security, accurate request handling,
    # and generating proper URLs in your application.
    app.wsgi_app = ProxyFix(app.wsgi_app)

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

    # Enforce foreign keys checking which in sqlite is turned off by default
    if "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"]:

        def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
            dbapi_con.execute("pragma foreign_keys=ON")

        with app.app_context():
            from sqlalchemy import event

            event.listen(db.engine, "connect", _fk_pragma_on_connect)
