from datetime import datetime
from extensions import db


class IncidentHistory(db.Model):
    __tablename__ = 'incident_history'
    
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('incidents.id'), nullable=False)
    action_taken = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    performed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    performer = db.relationship('User', foreign_keys=[performed_by], backref='performed_actions')
    
    def __repr__(self):
        return f'<IncidentHistory {self.id} - {self.action_taken}>'
