from datetime import datetime
import jwt
from flask import current_app as app
from alembic import op

# local
from app import db, bcrypt


class Discount(db.Model):
    """ Discount Model for storing Discount """

    __tablename__ = "discounts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    rate = db.Column(db.Float(), nullable=False)
    start_campaign_datetime = db.Column(db.DateTime, nullable=False)
    end_campaign_datetime = db.Column(db.DateTime, nullable=False)
    created_datetime = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_datetime = db.Column(
        db.DateTime, nullable=False,
        onupdate=datetime.now(), default=db.func.current_timestamp()
    )
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'),
                           nullable=False)

    def __init__(self, name,
                 start_campaign_datetime,
                 end_campaign_datetime,
                 product_id, rate):
        self.name = name
        self.start_campaign_datetime = start_campaign_datetime
        self.end_campaign_datetime = end_campaign_datetime
        self.created_datetime = datetime.now()
        self.product_id = product_id
        self.rate = rate

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Discount.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "rate": self.rate,
                    "start_campaign_datetime": self.start_campaign_datetime,
                    "end_campaign_datetime": self.end_campaign_datetime})
