from db import db

class CustomerModel(db.Model):
    __tablename__ = "customers"
    customer_id = db.Column(db.Integer, primary_key = True)
    uuid_customer = db.Column(db.String(36))
    name = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    is_vip = db.Column(db.Boolean)


