from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import stripe



app = Flask(__name__)
app.config.from_object(Config)

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_PATH'] = './app/static/uploads'

stripe.api_key='pk_test_51MwDx2Jk4MDHTRtHdqQMjaQSioYt10GJK7HaJ1bcFdLCHeWapu0MRrIRHOeRNzpIHMrn9UpTlTRdthuHqEtHu1qP00VNXa0Cvo'
stripe.api_key='sk_test_51MwDx2Jk4MDHTRtHDqT5s7hFk0QcHsuTt2yU0VZ93FQVTaXJinikAVViNBtz7m8ijgAfbk35OekMQEQ3YRIq30kH00SrF3lfXA'

db = SQLAlchemy(app)

migrate = Migrate(app,db)

login = LoginManager(app)

login.login_view = 'login'

login.login_message_view = 'login_message'

from app import routes, models
