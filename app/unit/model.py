from datetime import datetime
from app import db
from app.tenant.model import Tenant

tenancy_cycle = db.Table('tenancy_cycle',
    db.Column('unit_id', db.Integer, db.ForeignKey('unit.id'), primary_key=True),
    db.Column('tenant_id', db.Integer, db.ForeignKey('tenant.id'), primary_key=True),
    db.Column('cycle', db.Integer)
)
class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    annual_fee = db.Column(db.Integer)
    status = db.Column(db.String(255))
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'))
    tenant = db.relationship('Tenant', backref=db.backref('units', lazy=True))
    next_payment_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, name=None, annual_fee=None, status=None, property_id=None, tenant_id=None, date=None):
        self.name = name or self.name
        self.annual_fee = annual_fee or self.annual_fee
        self.status = status or self.status
        self.property_id = property_id or self.property_id
        self.tenant_id = tenant_id or self.tenant_id
        self.add_tenancy_cycle(date)
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        self.is_deleted = True
        self.updated_at = db.func.now()
        db.session.commit()
    
    def add_tenancy_cycle(self, date):
        if date:
            self.next_payment_date = date
            cycle = datetime.strptime(date, '%Y-%m-%d').timetuple().tm_yday
            existing_cycle = db.session.execute(tenancy_cycle.select().where(tenancy_cycle.c.unit_id == self.id).where(tenancy_cycle.c.tenant_id == self.tenant_id)).fetchone()
            if existing_cycle:
                db.session.execute(tenancy_cycle.update().where(tenancy_cycle.c.unit_id == self.id).where(tenancy_cycle.c.tenant_id == self.tenant_id).values(cycle=cycle))
            else:
                db.session.execute(tenancy_cycle.insert().values(unit_id=self.id, tenant_id=self.tenant_id, cycle=cycle))
            db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()
    
    @classmethod
    def get_by_tenant_id(cls, tenant_id):
        return cls.query.filter_by(tenant_id=tenant_id, is_deleted=False).all()
    
    @classmethod
    def create(cls, name, annual_fee, status, property_id, tenant_id, date):
        unit = cls(name=name, annual_fee=annual_fee, status=status, property_id=property_id, tenant_id=tenant_id)
        unit.save()
        unit.add_tenancy_cycle(date)
        return unit