# app/models/education_event.py

from app import db
from datetime import date, time

class EducationEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<EducationEvent {self.title} on {self.date}>'
