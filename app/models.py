from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin


db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    first_name = db.Column(db.String(45))

    product = db.relationship("Product", backref='added to cart')
    cart = db.relationship("Cart", backref='your cart')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String(500))
    price = db.column(db.Float, nullable=False)
    cart_items= db.relationship('Cart', backref='Product in cart')
   

    def __init__(self, img_url, description, price):
        self.img_url = img_url
        self.description = description
        self.price = price

class Cart(db.Model):
    id=db.Columm(db.Integer, primary_key=True)
    product_id=db.Column(db.Integer, db.ForeignKey('product.id'))
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
  


