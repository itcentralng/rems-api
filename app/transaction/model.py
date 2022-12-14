from datetime import datetime
from app import db
from app.unit.model import Unit
from app.tenant.model import Tenant

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
    unit = db.relationship('Unit', backref=db.backref('transactions', lazy=True))
    tenant = db.relationship('Tenant', backref=db.backref('transactions', lazy=True))
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), default='full')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, tenant_id, unit_id, amount):
        self.tenant_id = tenant_id or self.tenant_id
        self.unit_id = unit_id or self.unit_id
        self.amount = amount or self.amount
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        self.is_deleted = True
        self.updated_at = db.func.now()
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.join(Unit).filter(Unit.is_deleted==False, cls.is_deleted==False).all()
    
    @classmethod
    def get_by_tenant_id(cls, tenant_id):
        return cls.query.join(Unit).filter(Unit.is_deleted==False, cls.is_deleted==False, cls.tenant_id==tenant_id).all()
    
    @classmethod
    def get_by_unit_id(cls, unit_id):
        return cls.query.filter_by(unit_id=unit_id, is_deleted=False).all()
    
    @classmethod
    def get_recent_by_unit_id_and_tenant_id(cls, unit_id, tenant_id):
        return cls.query.filter_by(unit_id=unit_id, tenant_id=tenant_id, is_deleted=False).order_by(Transaction.created_at.desc()).first()

    @classmethod
    def get_total_tenancy_fee_not_paid(cls):
        current_year_paid_units = db.session.query(Transaction.unit_id).filter(Transaction.created_at >= datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)).all()
        return db.session.query(db.func.coalesce(db.func.sum(Unit.annual_fee), 0)).filter(Unit.is_deleted == False, Unit.next_payment_date <= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)).filter(Unit.id.notin_([unit.unit_id for unit in current_year_paid_units])).scalar()
    
    @classmethod
    def get_total_tenancy_due(cls):
        return db.session.query(db.func.coalesce(db.func.sum(Unit.annual_fee), 0)).filter(Unit.is_deleted == False, Unit.next_payment_date <= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)).scalar()
    
    @classmethod
    def get_total_tenancy_fee_paid_for_current_period(cls):
        return db.session.query(db.func.coalesce(db.func.sum(Transaction.amount), 0)).join(Unit).filter(Transaction.created_at >= datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0), Unit.is_deleted == False).scalar()

    @classmethod
    def get_total_tenancy_fee_paid(cls):
        return db.session.query(db.func.coalesce(db.func.sum(Transaction.amount), 0)).join(Unit).filter(Unit.is_deleted == False).scalar()
    
    @classmethod
    def create(cls, tenant_id, unit_id, amount):
        amount = float(amount)
        type = 'full'
        unit = Unit.get_by_id(unit_id)
        recent_payment = Transaction.get_recent_by_unit_id_and_tenant_id(unit_id, tenant_id)
        if recent_payment:
            if recent_payment.type == 'half':
                type = 'full'
                if unit.annual_fee/2 != amount:
                    return
            elif recent_payment.type == 'full':
                if unit.annual_fee/2 == amount:
                    type = 'half'
                elif unit.annual_fee == amount:
                    type = 'full'
                else:
                    return
        elif unit.annual_fee/2 == amount:
            type = 'half'
        elif unit.annual_fee == amount:
            type = 'full'
        else:
            return
        transaction = cls(tenant_id=tenant_id, unit_id=unit_id, amount=amount, type=type)
        transaction.save()
        return transaction