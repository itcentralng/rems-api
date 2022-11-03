from app import ma
from app.property.model import *

class PropertySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Property
        exclude = ('is_deleted',)
        include_fk = True
    images = ma.Nested('ImageSchema', many=True)
    units = ma.Nested('UnitSchema', many=True)
    agent = ma.Nested('AgentSchema', many=False)

class ImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Propertyimage