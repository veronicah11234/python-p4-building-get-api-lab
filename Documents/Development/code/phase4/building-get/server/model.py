# models.py

from app import db

class Bakery(db.Model):
    __tablename__ = 'bakeries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    baked_goods = db.relationship('BakedGood', backref='bakery')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'baked_goods': [baked_good.serialize() for baked_good in self.baked_goods]
        }

class BakedGood(db.Model):
    __tablename__ = 'baked_goods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'bakery_id': self.bakery_id
        }
