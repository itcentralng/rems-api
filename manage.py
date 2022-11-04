from datetime import datetime
from app import app
from app.property.model import Property

with app.app_context():
    print('Ready!')