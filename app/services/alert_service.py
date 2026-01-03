"""
Alert Service - Business logic for alert management
"""
from typing import List, Optional
from app.models.alert import Alert
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
