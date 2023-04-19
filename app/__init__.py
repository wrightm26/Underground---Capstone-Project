from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager



app = Flask(__name__)
app.config.from_object(Config)

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_PATH'] = './app/static/uploads'

db = SQLAlchemy(app)

migrate = Migrate(app,db)

login = LoginManager(app)

login.login_view = 'login'

login.login_message_view = 'login_message'

from app import routes, models
