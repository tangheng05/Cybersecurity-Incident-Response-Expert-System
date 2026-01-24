from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from datetime import datetime, timedelta
from sqlalchemy import func
from app.models.alert import Alert
from app.models.incident import Incident
from app.models.rule import Rule
from app.models.attack_type import AttackType
from app.utils.decorators import login_required
from extensions import db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = None  # No longer using WTForms
    
    # Handle alert submission
    if request.method == 'POST':
        try:
            # Build JSON from simple form fields
            raw_data = {
                "source_ip": request.form.get('source_ip')
            }
            
            # Add optional fields only if provided
            if request.form.get('failed_attempts'):
                raw_data['failed_attempts'] = int(request.form.get('failed_attempts'))
            if request.form.get('requests_per_second'):
                raw_data['requests_per_second'] = int(request.form.get('requests_per_second'))
            if request.form.get('target_service'):
                raw_data['target_service'] = request.form.get('target_service')
            if request.form.get('time_window'):
                raw_data['time_window'] = int(request.form.get('time_window'))
            
            alert = Alert(
                source_ip=request.form.get('source_ip'),
                destination_ip=None,
                alert_type='Analyzing',
                severity=request.form.get('severity'),
                raw_data=raw_data,
                status='new'
            )
            db.session.add(alert)
            db.session.flush()
            
            from app.services.alert_service import AlertService
            
            analysis = AlertService.analyze_and_create_incident(alert)
            
            if analysis['top_conclusion']:
                alert.alert_type = analysis['top_conclusion'].replace('_', ' ').title()
            
            db.session.commit()
            
            analysis_summary = {
                'alert_id': alert.id,
                'alert_type': alert.alert_type,
                'confidence': analysis['final_cf'],
                'matched_rules_count': len([t for t in analysis['trace'] if t.fired]),
                'recommended_actions': [],
                'severity': alert.severity,
                'source_ip': alert.source_ip
            }
            
            form = None
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Error: {str(e)}', 'danger')
            analysis_summary = None
    else:
        analysis_summary = None
    
    # Calculate statistics
    # Active incidents (new, analyzing, pending)
    active_incidents_count = Incident.query.filter(
        Incident.status.in_(['new', 'analyzing', 'pending'])
    ).count()
    
    # Pending alerts (status = 'new')
    pending_alerts_count = Alert.query.filter_by(status='new').count()
    
    # Resolved incidents today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    resolved_today_count = Incident.query.filter(
        Incident.status == 'resolved',
        Incident.resolved_at >= today_start
    ).count()
    
    # Active rules count
    active_rules_count = Rule.query.filter_by(is_active=True).count()
    
    # Recent alerts (last 10)
    recent_alerts = Alert.query.order_by(Alert.created_at.desc()).limit(10).all()
    
    # Attack type distribution for chart
    attack_type_stats = db.session.query(
        AttackType.name,
        func.count(Incident.id).label('count')
    ).join(Incident, Incident.attack_type_id == AttackType.id, isouter=True)\
     .group_by(AttackType.name).all()
    
    # Incident status distribution
    status_stats = db.session.query(
        Incident.status,
        func.count(Incident.id).label('count')
    ).group_by(Incident.status).all()
    
    # Recent incidents (last 5)
    recent_incidents = Incident.query.order_by(Incident.created_at.desc()).limit(5).all()
    
    return render_template(
        'dashboard/index.html',
        analysis_summary=analysis_summary,
        active_incidents_count=active_incidents_count,
        pending_alerts_count=pending_alerts_count,
        resolved_today_count=resolved_today_count,
        active_rules_count=active_rules_count,
        recent_alerts=recent_alerts,
        attack_type_stats=attack_type_stats,
        status_stats=status_stats,
        recent_incidents=recent_incidents
    )
