from flask import Blueprint, request
from app.route_guard import auth_required

from app.transaction.model import Transaction
from app.transaction.schema import TransactionSchema

from app.unit.model import *
from app.unit.schema import *

bp = Blueprint('unit', __name__)

@bp.post('/unit')
@auth_required()
def create_unit():
    name = request.json.get('name')
    annual_fee = request.json.get('annual_fee')
    status = request.json.get('status')
    property_id = request.json.get('property_id')
    tenant_id = request.json.get('tenant_id')
    date = request.json.get('date')
    unit = Unit.create(name, annual_fee, status, property_id, tenant_id, date)
    return UnitSchema().dump(unit), 201

@bp.get('/unit/<int:id>')
@auth_required()
def get_unit(id):
    unit = Unit.get_by_id(id)
    if unit is None:
        return {'message': 'Unit not found'}, 404
    recent_payment = Transaction.get_recent_by_unit_id_and_tenant_id(unit.id, unit.tenant_id)
    unitschema = UnitSchema().dump(unit)
    unitschema['recent_payment'] = TransactionSchema().dump(recent_payment)
    return unitschema, 200

@bp.put('/unit/<int:id>')
@auth_required()
def update_unit(id):
    unit = Unit.get_by_id(id)
    name = request.json.get('name')
    annual_fee = request.json.get('annual_fee')
    status = request.json.get('status')
    property_id = request.json.get('property_id')
    tenant_id = request.json.get('tenant_id')
    date = request.json.get('date')
    if unit is None:
        return {'message': 'Unit not found'}, 404
    unit.update(name, annual_fee, status, property_id, tenant_id, date)
    return UnitSchema().dump(unit), 200

@bp.delete('/unit/<int:id>')
@auth_required()
def delete_unit(id):
    unit = Unit.get_by_id(id)
    if unit is None:
        return {'message': 'Unit not found'}, 404
    unit.delete()
    return {'message': 'Unit deleted successfully'}, 200

@bp.get('/units')
@auth_required()
def get_units():
    units = Unit.get_all()
    return UnitSchema(many=True).dump(units), 200

@bp.patch('/unit/<int:id>')
@auth_required()
def add_tenancy_cycle(id):
    unit = Unit.get_by_id(id)
    if unit is None:
        return {'message': 'Unit not found'}, 404
    date = request.json.get('date')
    unit.add_tenancy_cycle(date)
    return UnitSchema().dump(unit), 200