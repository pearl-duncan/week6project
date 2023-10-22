from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash



db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    
    cart = db.relationship("Cart", backref='your_cart')

    def __init__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def compare_password(self, password):
        return check_password_hash(self.password, password)
    
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def addToCart(self, **kwargs):
        for key, value in kwargs.items():
            if key == "password":
                setattr(self, key, generate_password_hash(value))
            else:
                setattr(self, key, value)
        db.session.commit()

class Product(db.Model):
    id = db.Column(db.String, primary_key=True)
    img_url = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    


    cart_items= db.relationship('Cart', backref='Product_in_cart')
   
   

    def __init__(self, img_url, name, description, price, created_by):
        self.id = str(uuid4())
        self.img_url = img_url
        self.name = name
        self.description = description
        self.price = price
        self.created_by = created_by

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def to_response(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "img_url": self.img_url,
            "description": self.description,
            "price": self.price,
            "created_by": self.author.username,
            
        }

class Cart(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    product_id=db.Column(db.String, db.ForeignKey('product.id'))
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
  


