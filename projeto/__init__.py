import os

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite')
    )

    os.makedirs(app.instance_path, 0o777, True)

    @app.route("/hello")
    def hello():
        return "Hello World"

    from . import db
    db.init_app(app)

    return app
