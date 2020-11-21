from .. import db

class Schedules_common(db.Model):

    __tablename__ = "schedules_common"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    memo = db.Column(db.String(100), nullable=False)
    startdate = db.Column(db.String(100), nullable=False)
    enddate = db.Column(db.String(100), nullable=False)
    cycle = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    schedules_dates = db.relationship('Schedules_date', backref='schedules_codate', lazy=True)
    

    def __repr__(self):
        return "<schedules_common '{}'>".format(self.title)