from flask import Blueprint, request
from app.route_guard import auth_required

from app.transaction.model import *
from app.transaction.schema import *

bp = Blueprint('transaction', __name__)

@bp.post('/transaction')
@auth_required()
def create_transaction():
    tenant_id = request.json.get('tenant_id')
    unit_id = request.json.get('unit_id')
    amount = request.json.get('amount')
    next_payment_date = request.json.get('next_payment_date')
    transaction = Transaction.create(tenant_id, unit_id, amount)
    unit = Unit.get_by_id(unit_id)
    unit.add_tenancy_cycle(next_payment_date)
    return TransactionSchema().dump(transaction), 201

@bp.get('/transaction/<int:id>')
@auth_required()
def get_transaction(id):
    transaction = Transaction.get_by_id(id)
    if transaction is None:
        return {'message': 'Transaction not found'}, 404
    return TransactionSchema().dump(transaction), 200

@bp.put('/transaction/<int:id>')
@auth_required()
def update_transaction(id):
    transaction = Transaction.get_by_id(id)
    tenant_id = request.json.get('tenant_id')
    unit_id = request.json.get('unit_id')
    amount = request.json.get('amount')
    if transaction is None:
        return {'message': 'Transaction not found'}, 404
    transaction.update(tenant_id, unit_id, amount)
    return TransactionSchema().dump(transaction), 200

@bp.delete('/transaction/<int:id>')
@auth_required()
def delete_transaction(id):
    transaction = Transaction.get_by_id(id)
    if transaction is None:
        return {'message': 'Transaction not found'}, 404
    transaction.delete()
    return {'message': 'Transaction deleted successfully'}, 200

@bp.get('/transactions')
@auth_required()
def get_transactions():
    transactions = Transaction.get_all()
    return TransactionSchema(many=True).dump(transactions), 200

@bp.get('/transaction/report')
@auth_required()
def get_transaction_report():
    get_total_tenancy_fee_not_paid = Transaction.get_total_tenancy_fee_not_paid()
    get_total_tenancy_due = Transaction.get_total_tenancy_due()
    get_total_tenancy_fee_paid = Transaction.get_total_tenancy_fee_paid()
    get_total_tenancy_fee_paid_for_current_period = Transaction.get_total_tenancy_fee_paid_for_current_period()
    return {
        'notpaid': get_total_tenancy_fee_not_paid,
        'due': get_total_tenancy_due,
        'paid': get_total_tenancy_fee_paid,
        'paidforcurrentperiod': get_total_tenancy_fee_paid_for_current_period
    }, 200