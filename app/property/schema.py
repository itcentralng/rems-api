from app import ma
from app.property.model import *

class PropertySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Property
        exclude = ('is_deleted',)
    images = ma.Nested('ImageSchema', many=True)
    units = ma.Nested('UnitSchema', many=True)