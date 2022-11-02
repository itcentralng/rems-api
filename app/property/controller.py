from flask import Blueprint, request
from app.route_guard import auth_required

from app.property.model import *
from app.property.schema import *

bp = Blueprint('property', __name__)

@bp.post('/property')
@auth_required()
def create_property():
    name = request.json.get('name')
    address = request.json.get('address')
    state = request.json.get('state')
    lga = request.json.get('lga')
    images = request.json.get('images')
    property = Property.create(name, address, state, lga, images)
    return PropertySchema().dump(property), 201

@bp.get('/property/<int:id>')
@auth_required()
def get_property(id):
    property = Property.get_by_id(id)
    if property is None:
        return {'message': 'Property not found'}, 404
    return PropertySchema().dump(property), 200

@bp.patch('/property/<int:id>')
@auth_required()
def update_property(id):
    property = Property.get_by_id(id)
    name = request.json.get('name')
    address = request.json.get('address')
    state = request.json.get('state')
    lga = request.json.get('lga')
    images = request.json.get('images')
    if property is None:
        return {'message': 'Property not found'}, 404
    property.update(name, address, state, lga, images)
    return PropertySchema().dump(property), 200

@bp.delete('/property/<int:id>')
@auth_required()
def delete_property(id):
    property = Property.get_by_id(id)
    if property is None:
        return {'message': 'Property not found'}, 404
    property.delete()
    return {'message': 'Property deleted successfully'}, 200

@bp.get('/properties')
@auth_required()
def get_propertys():
    propertys = Property.get_all()
    return PropertySchema(many=True).dump(propertys), 200