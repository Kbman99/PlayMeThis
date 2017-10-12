from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager

from app import admin
from app.models import User
from app.views import main, user, error, api
from app.logger_setup import logger

from .toolbox import webhook


app = Flask(__name__)

app.config.from_object('app.config')

db = SQLAlchemy(app)
mail = Mail(app)
bcrypt = Bcrypt(app)
toolbar = DebugToolbarExtension(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userbp.signin'

app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
app.config['DEBUG_TB_PROFILER_ENABLED'] = True

app.register_blueprint(user.userbp)

webhook.setup_token()


@login_manager.user_loader
def load_user(email):
    return User.query.filter(User.email == email).first()
