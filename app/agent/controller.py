from flask import Blueprint

from app.agent.model import *
from app.agent.schema import *
bp = Blueprint('agent', __name__)

@bp.get('/index')
def index():
    return 'agent Works'