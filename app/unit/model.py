from app import db

class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    annual_fee = db.Column(db.Integer)
    status = db.Column(db.String(255))
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, name=None, annual_fee=None, status=None, property_id=None, tenant_id=None):
        self.name = name or self.name
        self.annual_fee = annual_fee or self.annual_fee
        self.status = status or self.status
        self.property_id = property_id or self.property_id
        self.tenant_id = tenant_id or self.tenant_id
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
    def create(cls, name, annual_fee, status, property_id, tenant_id):
        unit = cls(name=name, annual_fee=annual_fee, status=status, property_id=property_id, tenant_id=tenant_id)
        unit.save()
        return unit