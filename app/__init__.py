from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)


bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

products = {
        'phone': {
            'name': 'iphone 13 pro',
            'price': 13900,
            'adjustable_quantity': {
                'enabled': True,
                'minimum': 1,
                'maximum': 4
            },
        },
        'laptop': {
            'name': 'macbook',
            'price': 20000,
            'adjustable_quantity': {
                'enabled': True,
                'minimum': 1,
                'maximum': 4
            },
        },
        'watch': {
            'name': 'Apple Watch',
            'price': 10000,
            'adjustable_quantity': {
                'enabled': True,
                'minimum': 1,
                'maximum': 4
            },
        },
    }

from app import routes, models, errors
