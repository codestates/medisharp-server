from .. import db

class Schedules_common(db.Model):

    __tablename__ = "schedules_common"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    memo = db.Column(db.String(100), nullable=False)
    startdate = db.Column(db.String(100), nullable=False)
    enddate = db.Column(db.String(100), nullable=False)
    cycle = db.Column(db.Integer, nullable=False)

    def __init__(self):
      self.title = title
      self.users_id = users_id
      self.date = date
      self.memo = memo
      self.startdate = startdate
      self.enddate = enddate
      self.cycle = cycle

    def __repr__(self):
        return "<schedules_common '{}'>".format(self.title)
        
