from datetime import datetime
import jwt
from flask import current_app as app
from alembic import op
from sqlalchemy import and_


# local
from app import db, bcrypt
from models.DiscountModel import Discount

class Product(db.Model):
    """ Product Model used for accessing and manipulating data products """

    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_code = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)
    price = db.Column(db.Float(), nullable=False)
    stocks = db.Column(db.Float(), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    created_datetime = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_datetime = db.Column(
        db.DateTime, nullable=False,
        onupdate=datetime.now(), default=db.func.current_timestamp()
    )
    discount = db.relationship('Discount', backref='products', lazy="joined")

    def __init__(self, group_code, name, price, stocks, is_active=True):
        self.group_code = group_code
        self.name = name
        self.price = price
        self.stocks = stocks
        self.created_datetime = datetime.now()
        self.is_active = is_active

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        res = Product.query \
            .all()

        return res

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "stocks": self.stocks, "price": self.price, "discount": self.discount})
