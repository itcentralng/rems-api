from datetime import datetime
from app import db
from app.unit.model import Unit, tenancy_cycle
from app.tenant.model import Tenant

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
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
        return cls.query.filter_by(is_deleted=False).all()

    @classmethod
    def get_total_tenancy_fee_not_paid(cls):
        day_of_the_year = datetime.now().timetuple().tm_yday
        current_year_paid_units = db.session.query(Transaction.unit_id).filter(Transaction.created_at >= datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)).all()
        return db.session.query(db.func.sum(Unit.annual_fee)).join(tenancy_cycle, Unit.id == tenancy_cycle.c.unit_id).filter(tenancy_cycle.c.cycle <= day_of_the_year, Unit.id.notin_([unit.unit_id for unit in current_year_paid_units])).scalar()
    
    @classmethod
    def get_total_tenancy_due(cls):
        day_of_the_year = datetime.now().timetuple().tm_yday
        return db.session.query(db.func.sum(Unit.annual_fee)).join(tenancy_cycle, Unit.id == tenancy_cycle.c.unit_id).filter(Unit.is_deleted == False, tenancy_cycle.c.cycle <= day_of_the_year).scalar()
    
    @classmethod
    def get_total_tenancy_fee_paid_for_current_period(cls):
        return db.session.query(db.func.sum(Transaction.amount)).filter(Transaction.created_at >= datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)).scalar()

    @classmethod
    def get_total_tenancy_fee_paid(cls):
        return db.session.query(db.func.sum(Transaction.amount)).scalar()
    
    @classmethod
    def create(cls, tenant_id, unit_id, amount):
        transaction = cls(tenant_id=tenant_id, unit_id=unit_id, amount=amount)
        transaction.save()
        return transaction