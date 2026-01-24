from datetime import datetime
from extensions import db


class Incident(db.Model):
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.Integer, db.ForeignKey('alerts.id'), nullable=False, unique=True)
    attack_type_id = db.Column(db.Integer, db.ForeignKey('attack_types.id'), nullable=True)
    
    conclusions = db.Column(db.JSON, nullable=True)
    trace = db.Column(db.JSON, nullable=True)
    final_cf = db.Column(db.Float, nullable=True)
    
    matched_rules = db.Column(db.JSON, nullable=True)
    recommended_actions = db.Column(db.JSON, nullable=True)
    confidence_score = db.Column(db.Integer, default=0, nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='new', nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    resolved_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    history = db.relationship('IncidentHistory', backref='incident', lazy=True, cascade='all, delete-orphan')
    assigned_user = db.relationship('User', foreign_keys=[assigned_to], backref='assigned_incidents')
    
    def __repr__(self):
        return f'<Incident {self.id} - {self.status}>'
