from flask import Blueprint, request

from app.agent.model import *
from app.agent.schema import *
bp = Blueprint('agent', __name__)

@bp.post('/agent')
def create_agent():
    image = request.json.get('image')
    name = request.json.get('name')
    name = request.json.get('name')
    email = request.json.get('email')
    phone = request.json.get('phone')
    home_address = request.json.get('home_address')
    work_address = request.json.get('work_address')
    agent = Agent.create(image, name, email, phone, home_address, work_address)
    return AgentSchema().dump(agent), 201

@bp.get('/agent/<int:id>')
def get_agent(id):
    agent = Agent.get_by_id(id)
    if agent is None:
        return {'message': 'Agent not found'}, 404
    return AgentSchema().dump(agent), 200

@bp.patch('/agent/<int:id>')
def update_agent(id):
    agent = Agent.get_by_id(id)
    if agent is None:
        return {'message': 'Agent not found'}, 404
    image = request.json.get('image')
    name = request.json.get('name')
    email = request.json.get('email')
    phone = request.json.get('phone')
    home_address = request.json.get('home_address')
    work_address = request.json.get('work_address')
    agent.update(image, name, email, phone, home_address, work_address)
    return AgentSchema().dump(agent), 200

@bp.delete('/agent/<int:id>')
def delete_agent(id):
    agent = Agent.get_by_id(id)
    if agent is None:
        return {'message': 'Agent not found'}, 404
    agent.delete()
    return {'message': 'Agent deleted successfully'}, 200

@bp.get('/agents')
def get_agents():
    agents = Agent.get_all()
    return AgentSchema(many=True).dump(agents), 200