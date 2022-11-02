from app import db
from app.unit.model import Unit

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    lga = db.Column(db.String(255), nullable=False)
    images = db.relationship('Propertyimage', backref='property', lazy=True)
    units = db.relationship('Unit', backref='property', lazy=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, name=None, address=None, state=None, lga=None, images=[]):
        self.name = name or self.name
        self.address = address or self.address
        self.state = state or self.state
        self.lga = lga or self.lga
        for image in images:
            self.add_image(image)
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        self.is_deleted = True
        self.updated_at = db.func.now()
        db.session.commit()

    def add_image(self, image):
        Propertyimage.create(image, self.id)
        db.session.commit()
    
    def remove_image(self, image_id):
        image = Propertyimage.get_by_id(image_id)
        self.images.remove(image)
        image.delete()
        db.session.commit()
    
    def add_unit(self, unit):
        self.units.append(unit)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()
    
    @classmethod
    def create(cls, name, address, state, lga, images=[]):
        property = cls(name=name, address=address, state=state, lga=lga)
        property.save()
        for image in images:
            property.add_image(image)
        return property

class Propertyimage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, image=None):
        self.image = image or self.image
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()
    
    @classmethod
    def create(cls, image, property_id):
        propertyimage = cls(image=image, property_id=property_id)
        propertyimage.save()
        return propertyimage