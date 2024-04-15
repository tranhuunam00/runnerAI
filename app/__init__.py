from flask import Flask

import os


def create_app(debug: bool = False):
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", False)
    if FLASK_DEBUG:
        debug = FLASK_DEBUG

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
        static_url_path="/",
    )

    app.app_context().push()

    if debug:
        from app.config.dev import DevConfig

        app.config.from_object(DevConfig)
    else:
        from app.config.prod import ProdConfig

        app.config.from_object(ProdConfig)

    # Uncomment to enable logger
    # from app.utils.logger import setup_flask_logger
    # setup_flask_logger()

    # Initialize extensions
    from app.extensions import cors, cache, limiter

    cors.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)

    # Register blueprints or routes
    from app.routes import face_bp, bib_bp

    app.register_blueprint(face_bp)
    app.register_blueprint(bib_bp)

    # Global Ratelimit Checker
    # this is used because auto_check is set to 'False'
    app.before_request(lambda: limiter.check())

    return app
