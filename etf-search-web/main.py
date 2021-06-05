import os

from flask import Flask
import routes
import logging

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(routes.bp)

    return app

if __name__ == '__main__':


    app = create_app()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    app.logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler('app.log', mode='w')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(stream_handler)
    app.logger.addHandler(file_handler)
    app.logger.info(f"Flask app started with {app}")
    app.run()