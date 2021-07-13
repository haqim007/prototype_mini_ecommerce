from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# local import
from instance.config import app_config


# init bcrypt
bcrypt = Bcrypt()
# init sql-alchemy
db = SQLAlchemy()

"""
The create_app function wraps the creation of a new Flask object,
and returns it after it's loaded up with configuration settings using
app.config and connected to the DB using db.init_app(app).
"""


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # register blueprint
    from middleware.Auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    from middleware.Products import products_blueprint
    app.register_blueprint(products_blueprint, url_prefix="/product")
    from middleware.Discount import discounts_blueprint
    app.register_blueprint(discounts_blueprint, url_prefix="/discount")

    return app
