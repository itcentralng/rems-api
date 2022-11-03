from app import ma
from app.unit.model import *

class UnitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Unit
        exclude = ('is_deleted',)
        include_fk = True
    tenant = ma.Nested('TenantSchema')