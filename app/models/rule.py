from datetime import datetime
from extensions import db


class Rule(db.Model):
    __tablename__ = 'rules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    attack_type_id = db.Column(db.Integer, db.ForeignKey('attack_types.id'), nullable=False)
    
    symbolic_conditions = db.Column(db.JSON, nullable=True)
    conclusion = db.Column(db.String(100), nullable=True)
    cf = db.Column(db.Float, nullable=True)
    
    conditions = db.Column(db.JSON, nullable=True)
    actions = db.Column(db.JSON, nullable=True)
    priority = db.Column(db.String(20), default='medium', nullable=False)
    severity_score = db.Column(db.Integer, default=5, nullable=False)
    match_threshold = db.Column(db.Float, default=0.7, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Rule {self.name}>'
