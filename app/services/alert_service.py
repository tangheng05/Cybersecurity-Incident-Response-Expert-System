"""
Alert Service - Business logic for alert management
"""
from typing import List, Optional, Dict
from app.models.alert import Alert
from app.models.incident import Incident
from extensions import db
from datetime import datetime


class AlertService:
    """Service class for Alert CRUD operations"""
    
    @staticmethod
    def get_all(status: Optional[str] = None) -> List[Alert]:
        """
        Get all alerts, optionally filtered by status
        
        Args:
            status: Filter by status (new/processed/ignored)
            
        Returns:
            List of Alert objects ordered by timestamp descending
        """
        query = Alert.query
        
        if status:
            query = query.filter_by(status=status)
        
        return query.order_by(Alert.timestamp.desc()).all()
    
    @staticmethod
    def get_by_id(alert_id: int) -> Optional[Alert]:
        """Get alert by ID"""
        return Alert.query.get(alert_id)
    
    @staticmethod
    def create(data: dict) -> Alert:
        """
        Create new alert
        
        Args:
            data: Dict with keys: source_ip, destination_ip, alert_type, 
                  severity, raw_data
        """
        alert = Alert(
            timestamp=datetime.utcnow(),
            source_ip=data.get('source_ip'),
            destination_ip=data.get('destination_ip'),
            alert_type=data.get('alert_type', 'unknown'),
            severity=data.get('severity', 'medium'),
            raw_data=data.get('raw_data', {}),
            status='new'
        )
        
        db.session.add(alert)
        db.session.commit()
        
        return alert
    
    @staticmethod
    def analyze_and_create_incident(alert: Alert) -> Dict:
        """
        Analyze alert using forward-chaining inference engine
        and create incident record
        
        Args:
            alert: Alert object to analyze
            
        Returns:
            Dict with analysis results and incident
        """
        from app.services.inference_engine import InferenceEngine
        from app.services.fact_extractor import FactExtractor
        from app.models.attack_type import AttackType
        from app.models.rule import Rule
        
        facts = FactExtractor.extract_facts(alert)
        
        active_rules = Rule.query.filter_by(is_active=True).all()
        rule_models = InferenceEngine.load_rules_from_db(active_rules)
        
        conclusions_dict, trace = InferenceEngine.infer(facts, rule_models)
        
        top_conclusion = None
        top_cf = 0.0
        attack_type_id = None
        
        if conclusions_dict:
            sorted_conclusions = sorted(conclusions_dict.items(), key=lambda x: x[1], reverse=True)
            top_conclusion_name = sorted_conclusions[0][0]
            top_cf = sorted_conclusions[0][1]
            
            conclusion_to_attack = {
                'brute_force_attack': 'brute_force',
                'credential_stuffing': 'brute_force',
                'ddos_attack': 'ddos',
                'apt_attack': 'unauthorized_access'
            }
            
            attack_name = conclusion_to_attack.get(top_conclusion_name)
            if attack_name:
                attack_type = AttackType.query.filter_by(name=attack_name).first()
                if attack_type:
                    attack_type_id = attack_type.id
        
        explanation_result = InferenceEngine.explain(top_conclusion_name, trace) if top_conclusion_name else {}
        explanation = explanation_result.get('summary', 'No conclusion reached')
        
        incident = Incident(
            alert_id=alert.id,
            attack_type_id=attack_type_id,
            conclusions=[{'conclusion': k, 'cf': v} for k, v in conclusions_dict.items()],
            trace=trace.to_dict(),
            final_cf=top_cf,
            explanation=explanation,
            status='new'
        )
        
        db.session.add(incident)
        alert.status = 'processed'
        db.session.commit()
        
        return {
            'incident': incident,
            'top_conclusion': top_conclusion_name,
            'final_cf': top_cf,
            'explanation': explanation,
            'facts': list(facts),
            'trace': trace.to_dict()
        }
    
    @staticmethod
    def update_status(alert: Alert, status: str) -> Alert:
        """Update alert status"""
        alert.status = status
        db.session.commit()
        return alert
    
    @staticmethod
    def delete(alert: Alert) -> None:
        """Delete alert"""
        db.session.delete(alert)
        db.session.commit()

