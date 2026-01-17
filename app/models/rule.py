from datetime import datetime
from extensions import db


class Rule(db.Model):
    __tablename__ = 'rules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    attack_type_id = db.Column(db.Integer, db.ForeignKey('attack_types.id'), nullable=False)
    conditions = db.Column(db.JSON, nullable=False)  # JSON storage for flexible conditions
    actions = db.Column(db.JSON, nullable=False)  # JSON array of action strings
    priority = db.Column(db.String(20), default='medium', nullable=False)  # high, medium, low
    severity_score = db.Column(db.Integer, default=5, nullable=False)  # 1-10
    match_threshold = db.Column(db.Float, default=0.7, nullable=False)  # 0.0-1.0, percentage of conditions that must match
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Rule {self.name}>'
