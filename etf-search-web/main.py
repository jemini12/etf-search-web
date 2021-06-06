import os

from flask import Flask
import routes
import logging
import config

def create_app(development_mode=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    app.logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler('app.log', mode='w')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(stream_handler)
    app.logger.addHandler(file_handler)
    app.logger.info("Flask app started with {app}")

    if development_mode is None:
        app.config.from_object(config.DevelopmentConfig)
    elif development_mode == "production":
        app.config.from_object(config.ProductionConfig)
    else:
        app.config.from_object(config.DevelopmentConfig)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(routes.bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port='8080')