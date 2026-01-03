from extensions import db


class AttackType(db.Model):
    __tablename__ = 'attack_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # brute_force, ddos
    description = db.Column(db.Text, nullable=True)
    severity_level = db.Column(db.Integer, default=5, nullable=False)  # 1-10
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    rules = db.relationship('Rule', backref='attack_type', lazy=True, cascade='all, delete-orphan')
    incidents = db.relationship('Incident', backref='attack_type', lazy=True)
    
    def __repr__(self):
        return f'<AttackType {self.name}>'
