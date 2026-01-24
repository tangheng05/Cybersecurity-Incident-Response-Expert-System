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
    def _generate_recommended_actions(conclusion: str, cf: float) -> list:
        """Generate recommended actions based on attack conclusion and CF"""
        if not conclusion:
            return ['Monitor alert for further activity', 'Review system logs']
        
        actions_map = {
            'brute_force_attack': [
                'Block source IP address immediately',
                'Enable account lockout after failed attempts',
                'Review authentication logs',
                'Implement rate limiting on login endpoints',
                'Enable multi-factor authentication'
            ],
            'credential_stuffing': [
                'Block source IP address',
                'Force password reset for affected accounts',
                'Implement CAPTCHA on login forms',
                'Monitor for lateral movement',
                'Check for compromised credentials in breach databases'
            ],
            'ddos_attack': [
                'Activate DDoS mitigation service',
                'Rate limit incoming connections',
                'Block malicious IP ranges',
                'Scale infrastructure resources',
                'Contact ISP for upstream filtering'
            ],
            'apt_attack': [
                'Isolate affected systems immediately',
                'Conduct full forensic analysis',
                'Review network traffic for data exfiltration',
                'Reset credentials for all privileged accounts',
                'Engage incident response team'
            ],
            'sql_injection_attack': [
                'Block malicious IP address immediately',
                'Review and sanitize all database queries',
                'Enable Web Application Firewall (WAF)',
                'Check database logs for unauthorized access',
                'Implement parameterized queries',
                'Review application input validation'
            ],
            'xss_attack': [
                'Block malicious IP address',
                'Sanitize all user inputs',
                'Implement Content Security Policy (CSP)',
                'Review and encode output data',
                'Enable XSS protection headers',
                'Audit web application code'
            ],
            'port_scan_attack': [
                'Block source IP address',
                'Review firewall rules',
                'Enable port scan detection',
                'Monitor for follow-up attacks',
                'Restrict unnecessary open ports',
                'Review network segmentation'
            ],
            'malware_attack': [
                'Isolate infected systems immediately',
                'Run full antivirus scan',
                'Block malicious file hashes',
                'Review endpoint protection logs',
                'Check for lateral movement',
                'Restore from clean backup if necessary'
            ],
            'phishing_attack': [
                'Block sender email address',
                'Alert affected users',
                'Review email security policies',
                'Implement email authentication (SPF, DKIM, DMARC)',
                'Conduct security awareness training',
                'Check for compromised credentials'
            ],
            'privilege_escalation_attack': [
                'Revoke elevated privileges immediately',
                'Review user access logs',
                'Reset affected account credentials',
                'Audit privilege assignment policies',
                'Enable privileged access monitoring',
                'Investigate root cause'
            ],
            'data_exfiltration_attack': [
                'Block data transfer immediately',
                'Isolate affected systems',
                'Review Data Loss Prevention (DLP) logs',
                'Identify exfiltrated data',
                'Notify security team and management',
                'Conduct forensic analysis',
                'Implement egress filtering'
            ]
        }
        
        base_actions = actions_map.get(conclusion, ['Investigate alert', 'Review logs'])
        
        if cf >= 0.9:
            return ['🚨 HIGH PRIORITY: ' + base_actions[0]] + base_actions[1:3]
        elif cf >= 0.7:
            return base_actions[:3]
        else:
            return base_actions[:2] + ['Continue monitoring']
    
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
        
        top_conclusion_name = None
        top_cf = 0.0
        attack_type_id = None
        
        if conclusions_dict:
            # Filter out None/NULL conclusions before sorting
            valid_conclusions = {k: v for k, v in conclusions_dict.items() if k is not None}
            
            if valid_conclusions:
                sorted_conclusions = sorted(valid_conclusions.items(), key=lambda x: x[1], reverse=True)
                top_conclusion_name = sorted_conclusions[0][0]
                top_cf = sorted_conclusions[0][1]
            
            conclusion_to_attack = {
                'brute_force_attack': 'brute_force',
                'credential_stuffing': 'brute_force',
                'ddos_attack': 'ddos',
                'apt_attack': 'unauthorized_access',
                'sql_injection_attack': 'sql_injection',
                'xss_attack': 'xss',
                'port_scan_attack': 'port_scan',
                'malware_attack': 'malware',
                'phishing_attack': 'phishing',
                'privilege_escalation_attack': 'privilege_escalation',
                'data_exfiltration_attack': 'data_exfiltration'
            }
            
            attack_name = conclusion_to_attack.get(top_conclusion_name)
            if attack_name:
                attack_type = AttackType.query.filter_by(name=attack_name).first()
                if attack_type:
                    attack_type_id = attack_type.id
        
        explanation_result = InferenceEngine.explain(top_conclusion_name, trace) if top_conclusion_name else {}
        explanation = explanation_result.get('summary', 'No conclusion reached')
        
        recommended_actions = AlertService._generate_recommended_actions(top_conclusion_name, top_cf)
        
        incident = Incident(
            alert_id=alert.id,
            attack_type_id=attack_type_id,
            conclusions=[{'conclusion': k, 'cf': v} for k, v in conclusions_dict.items()],
            trace=trace.to_dict(),
            final_cf=top_cf,
            explanation=explanation,
            recommended_actions=recommended_actions,
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
            'recommended_actions': recommended_actions,
            'facts': list(facts),
            'trace': trace.to_dict(),
            'fired_rules': trace.fired_rules,
            'trace_object': trace
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

