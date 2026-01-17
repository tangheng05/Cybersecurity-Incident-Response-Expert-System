from datetime import datetime
from extensions import db


class Alert(db.Model):
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    source_ip = db.Column(db.String(45), nullable=True)  # IPv4 or IPv6
    destination_ip = db.Column(db.String(45), nullable=True)
    alert_type = db.Column(db.String(50), nullable=False)  # Type of alert
    severity = db.Column(db.String(20), default='medium', nullable=False)  # low, medium, high, critical
    raw_data = db.Column(db.JSON, nullable=True)  # Flexible JSON storage for alert data
    status = db.Column(db.String(20), default='new', nullable=False)  # new, processed, ignored
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    incident = db.relationship('Incident', backref='alert', uselist=False, lazy=True)
    
    def __repr__(self):
        return f'<Alert {self.id} - {self.alert_type}>'
