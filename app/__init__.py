from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS

# App Config
app = Flask(__name__, )
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

# Flask-Upload
from flask_uploads import UploadSet, IMAGES, configure_uploads
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


# Celery
from app.celery import make_celery
celery = make_celery(app)

# Database
from config import secret
app.secret_key = secret
migrate = Migrate(app, db)


# Controllers
from app.user.controller import bp as user_bp
app.register_blueprint(user_bp)
from app.agent.controller import bp as agent_bp
app.register_blueprint(agent_bp)
from app.upload.controller import bp as upload_bp
app.register_blueprint(upload_bp)

# Error handlers
from .error_handlers import *