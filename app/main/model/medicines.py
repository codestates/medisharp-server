from .. import db, flask_bcrypt
from app.main.model.schedules_common import Schedules_common

schedules_medicines = db.Table('schedules_medicines',
    db.Column('schedules_common_id', db.Integer, db.ForeignKey('schedules_common.id')),
    db.Column('medicines_id', db.Integer, db.ForeignKey('medicines.id'))
)

class Medicines(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "medicines"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    image_dir = db.Column(db.String(100), nullable=False)
    effect = db.Column(db.Text, nullable=False)
    capacity = db.Column(db.Text, nullable=False)
    validity = db.Column(db.String(100), nullable=False)
    camera = db.Column(db.Boolean, nullable=False)
    users_id = db.Column(db.Integer, nullable=False)
    timetotake = db.relationship('Schedules_common', secondary=schedules_medicines, backref=db.backref('ttt', lazy='dynamic'))

    def __init__(self, name, title, image_dir, effect, capacity, validity, camera, users_id):
      self.name = name
      self.title = title
      self.image_dir = image_dir
      self.effect = effect
      self.capacity = capacity
      self.validity = validity
      self.camera = camera
      self.users_id = users_id

    def __repr__(self):
        return "<medicines '{}'>".format(self.name)
