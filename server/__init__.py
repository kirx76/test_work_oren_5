from flask import Flask
from flask_restx import Api, Resource

from . import user


# ---------------------------------------------------------------------------
def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.debug = True

    for m in (user,):
        api.add_namespace(m.api, path='/api')

    return app


# ---------------------------------------------------------------------------
def main():
    app = create_app()
    app.run()
