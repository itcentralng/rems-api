from app import db

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    phone = db.Column(db.String, unique=True)
    home_address = db.Column(db.String, default='')
    work_address = db.Column(db.String, default='')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, image=None, name=None, email=None, phone=None, home_address=None, work_address=None):
        self.image = image or self.image
        self.name = name or self.name
        self.email = email or self.email
        self.phone = phone or self.phone
        self.home_address = home_address or self.home_address
        self.work_address = work_address or self.work_address
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        self.is_deleted = True
        self.email = None
        self.phone = None
        self.updated_at = db.func.now()
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()
    
    @classmethod
    def create(cls, image, name, email, phone, home_address, work_address):
        agent = cls(image=image, name=name, email=email, phone=phone, home_address=home_address, work_address=work_address)
        agent.save()
        return agent