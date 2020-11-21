from .. import db
from datetime import datetime

class Schedules_date(db.Model):

    __tablename__ = "schedules_date"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Time, nullable=False)
    check = db.Column(db.Boolean, nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    schedules_common_id = db.Column(db.Integer, db.ForeignKey('schedules_common.id'), nullable=False)

    def __init__(self, year, month, date, time, check, users_id, schedules_common_id):
      self.year = year
      self.month = month
      self.date = date
      self.time = time
      self.check = check
      self.users_id = users_id
      self.schedules_common_id = schedules_common_id

    def __repr__(self):
        return "<schedules_date '{}'>".format(self.year)
