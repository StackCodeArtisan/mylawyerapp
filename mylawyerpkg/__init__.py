import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from mylawyerpkg import config
from mylawyerpkg.models import db
from mylawyerpkg import forms
from dotenv import load_dotenv
load_dotenv()

csrf = CSRFProtect()
mail = Mail()


def create_app():

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('config.py')
    app.config.from_object(config.BaseConfig)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['ADMIN_EMAIL'] = os.getenv('ADMIN_EMAIL')
    app.config['ADMIN_PASSWORD'] = os.getenv('ADMIN_PASSWORD')

    db.init_app(app)
    migrate = Migrate(app,db)
    csrf.init_app(app)
    mail.init_app(app)
  
  

    return app
app = create_app()

from mylawyerpkg import admin_routes, lawyer_routes, payment_routes, user_routes, landing_page_routes, admin_routes
