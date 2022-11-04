from flask import Blueprint, request
from app.route_guard import auth_required

from app.tenant.model import *
from app.tenant.schema import *
from app.transaction.model import Transaction
from app.transaction.schema import TransactionSchema
from app.unit.model import Unit
from app.unit.schema import UnitSchema

bp = Blueprint('tenant', __name__)

@bp.post('/tenant')
@auth_required()
def create_tenant():
    name = request.json.get('name')
    phone = request.json.get('phone')
    tenant = Tenant.create(name, phone)
    return TenantSchema().dump(tenant), 201

@bp.get('/tenant/<int:id>')
@auth_required()
def get_tenant(id):
    tenant = Tenant.get_by_id(id)
    if tenant is None:
        return {'message': 'Tenant not found'}, 404
    units = Unit.get_by_tenant_id(id)
    transactions = Transaction.get_by_tenant_id(id)
    tenant_schema = TenantSchema().dump(tenant)
    tenant_schema['units'] = UnitSchema(many=True).dump(units)
    tenant_schema['transactions'] = TransactionSchema(many=True).dump(transactions)
    return tenant_schema, 200

@bp.put('/tenant/<int:id>')
@auth_required()
def update_tenant(id):
    tenant = Tenant.get_by_id(id)
    name = request.json.get('name')
    phone = request.json.get('phone')
    if tenant is None:
        return {'message': 'Tenant not found'}, 404
    tenant.update(name, phone)
    return TenantSchema().dump(tenant), 200

@bp.delete('/tenant/<int:id>')
@auth_required()
def delete_tenant(id):
    tenant = Tenant.get_by_id(id)
    if tenant is None:
        return {'message': 'Tenant not found'}, 404
    tenant.delete()
    return {'message': 'Tenant deleted successfully'}, 200

@bp.get('/tenants')
@auth_required()
def get_tenants():
    tenants = Tenant.get_all()
    return TenantSchema(many=True).dump(tenants), 200