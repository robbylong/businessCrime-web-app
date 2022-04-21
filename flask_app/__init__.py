import dash
import dash_bootstrap_components as dbc
from flask import Flask
from flask.helpers import get_root_path
from flask_login import LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from pathlib import Path
import pandas as pd

app = Flask(__name__)
csrf = CSRFProtect()
csrf._exempt_views.add('dash.dash.dispatch')
db = SQLAlchemy()
login_manager = LoginManager()
photos = UploadSet('photos', IMAGES)

bcrypt = Bcrypt(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True

app.config['MAIL_USERNAME'] = 'violetliu74590@gmail.com'
app.config['MAIL_PASSWORD'] = 'biedanxin137'
mail = Mail(app)


def create_app(config_class_name):
    """
    Initialise the Flask application.
    :type config_class_name: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_class_name)

    register_dashapp(app)

    csrf.init_app(app)
    db.init_app(app)
    configure_uploads(app, photos)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    with app.app_context():
        from flask_app.models import User, Profile, Region
        db.create_all()
        add_region_data(db)
        # add_profession_data(db)

    from flask_app.main.routes import main_bp
    app.register_blueprint(main_bp)

    from flask_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app


def add_region_data(db_name):
    """ Adds the list of countries to the NOCRegion table to the database.
    :param db_name: the SQLite database initialised for the Flask app
    :type db_name: SQLAlchemy object
    """
    filename = Path(__file__).parent.joinpath('businessCrime_dash_app/data', 'regions.csv')
    df = pd.read_csv(filename, usecols=['region'])
    df.dropna(axis=0, inplace=True)
    df.drop_duplicates(subset=['region'], keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['id'] = df.index
    df.to_sql(name='region', con=db.engine, if_exists='replace', index=False)


def add_profession_data(db_name):
    """ Adds the list of professions to the database.
    :param db_name: the SQLite database initialised for the Flask app
    :type db_name: SQLAlchemy object
    """
    df = ['student', 'police officer', 'crime justice worker', 'citizen']
    df.to_sql(name='profession', con=db.engine, if_exists='replace', index=False)


def register_dashapp(app):
    """ Registers the Dash app in the Flask app and make it accessible on the route /dashboard/ """
    from flask_app.businessCrime_dash_app import layout
    from flask_app.businessCrime_dash_app.callbacks import register_callbacks

    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dashapp = dash.Dash(__name__,
                        server=app,
                        url_base_pathname='/dashboard/',
                        assets_folder=get_root_path(__name__) + '/dashboard/assets/',
                        meta_tags=[meta_viewport],
                        external_stylesheets=[dbc.themes.SKETCHY])

    with app.app_context():
        dashapp.title = 'Dashboard'
        dashapp.layout = layout.layout
        register_callbacks(dashapp)

    # Protects the views with Flask-Login
    _protect_dash_views(dashapp)


def _protect_dash_views(dash_app):
    """ Protects Dash views with Flask-Login"""
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.routes_pathname_prefix):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])
