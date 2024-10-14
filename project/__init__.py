import logging
import os

from flask import Flask
from flask_cors import CORS
from project.config import config

cors = CORS()

def create_app(config_name=None):
    """create a factory function"""
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "development")

    app = Flask(__name__)

    with app.app_context():
        app.config.from_object(config[config_name])

        app.logger.setLevel(logging.INFO)
        cors.init_app(app)
        from project.apis import api

        api.init_app(app)

        @app.shell_context_processor
        def ctx():  # pragma: no cover
            return {"app": app}

    return app
