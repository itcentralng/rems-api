from datetime import datetime
from app import app
from app.property.model import Property

with app.app_context():
    properties = Property.query.filter(Property.is_deleted == True).all()
    for property in properties:
        for unit in property.units:
            unit.delete()
    print('Ready!')