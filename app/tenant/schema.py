from app import ma
from app.tenant.model import *

class TenantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tenant
        exclude = ('is_deleted',)