from app import ma
from app.transaction.model import *

class TransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transaction
        exclude = ('is_deleted',)
    unit = ma.Nested('UnitSchema', only=('id', 'name', 'property_id'))
    tenant = ma.Nested('TenantSchema', only=('id', 'name', 'phone'))