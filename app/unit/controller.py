from flask import Blueprint, request
from app.route_guard import auth_required

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
    unit = Unit.create(name, annual_fee, status, property_id, tenant_id)
    return UnitSchema().dump(unit), 201

@bp.get('/unit/<int:id>')
@auth_required()
def get_unit(id):
    unit = Unit.get_by_id(id)
    if unit is None:
        return {'message': 'Unit not found'}, 404
    return UnitSchema().dump(unit), 200

@bp.put('/unit/<int:id>')
@auth_required()
def update_unit(id):
    unit = Unit.get_by_id(id)
    name = request.json.get('name')
    annual_fee = request.json.get('annual_fee')
    status = request.json.get('status')
    property_id = request.json.get('property_id')
    tenant_id = request.json.get('tenant_id')
    if unit is None:
        return {'message': 'Unit not found'}, 404
    unit.update(name, annual_fee, status, property_id, tenant_id)
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