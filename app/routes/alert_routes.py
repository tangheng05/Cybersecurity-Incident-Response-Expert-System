"""
Alert Routes - HTTP endpoints for alert management and analysis
"""
import json
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.models.alert import Alert
from app.models.incident import Incident
from app.forms.alert_forms import AlertForm
from app.services.alert_service import AlertService
from app.services.inference_engine import InferenceEngine
from app.utils.decorators import login_required, role_required
from extensions import db

alert_bp = Blueprint('alerts', __name__, url_prefix='/alerts')


@alert_bp.route('/')
@login_required
def index():
    """List all alerts - accessible by all logged-in users"""
    # Get filter from query params
    status_filter = request.args.get('status', None)
    
    alerts = AlertService.get_all(status=status_filter)
    
    return render_template('alerts/index.html', alerts=alerts, current_filter=status_filter)


@alert_bp.route('/<int:alert_id>')
@login_required
def detail(alert_id: int):
    """View alert details with analysis results"""
    alert = AlertService.get_by_id(alert_id)
    if not alert:
        flash('Alert not found.', 'danger')
        return redirect(url_for('alerts.index'))
    
    # Get associated incident if exists
    incident = Incident.query.filter_by(alert_id=alert_id).first()
    
    return render_template('alerts/detail.html', alert=alert, incident=incident)


@alert_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create and analyze new alert - All users can submit"""
    form = AlertForm()
    
    if form.validate_on_submit():
        try:
            # Build raw_data from form fields
            raw_data = {
                'source_ip': form.source_ip.data,
                'description': form.description.data
            }
            
            # Add optional fields if provided
            if form.failed_attempts.data:
                raw_data['failed_attempts'] = form.failed_attempts.data
            if form.target_service.data:
                raw_data['target_service'] = form.target_service.data
            if form.requests_per_second.data:
                raw_data['requests_per_second'] = form.requests_per_second.data
            if form.time_window.data:
                raw_data['time_window'] = form.time_window.data
            
            # Create alert
            alert = AlertService.create({
                'source_ip': form.source_ip.data,
                'destination_ip': form.destination_ip.data or None,
                'alert_type': form.alert_type.data,
                'severity': form.severity.data,
                'raw_data': raw_data
            })
            
            # Analyze alert with inference engine
            analysis_result = InferenceEngine.analyze_alert(alert)
            
            # Create incident from analysis
            incident = Incident(
                alert_id=alert.id,
                attack_type_id=analysis_result['attack_type_id'],
                matched_rules=analysis_result['matched_rules'],
                recommended_actions=analysis_result['recommended_actions'],
                confidence_score=analysis_result['confidence_score'],
                explanation=analysis_result['explanation'],
                status='new',
                assigned_to=session.get('user_id')
            )
            
            db.session.add(incident)
            
            # Update alert status
            alert.status = 'processed'
            
            db.session.commit()
            
            flash(f'Alert analyzed successfully! Confidence: {analysis_result["confidence_score"]}%', 'success')
            return redirect(url_for('alerts.detail', alert_id=alert.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error processing alert: {str(e)}', 'danger')
    
    return render_template('alerts/create.html', form=form)


@alert_bp.route('/<int:alert_id>/analyze', methods=['POST'])
@role_required('admin', 'analyst')
def analyze(alert_id: int):
    """Re-analyze an existing alert"""
    alert = AlertService.get_by_id(alert_id)
    if not alert:
        flash('Alert not found.', 'danger')
        return redirect(url_for('alerts.index'))
    
    try:
        # Re-analyze
        analysis_result = InferenceEngine.analyze_alert(alert)
        
        # Update or create incident
        incident = Incident.query.filter_by(alert_id=alert_id).first()
        
        if incident:
            incident.matched_rules = analysis_result['matched_rules']
            incident.recommended_actions = analysis_result['recommended_actions']
            incident.confidence_score = analysis_result['confidence_score']
            incident.explanation = analysis_result['explanation']
            incident.attack_type_id = analysis_result['attack_type_id']
        else:
            incident = Incident(
                alert_id=alert.id,
                attack_type_id=analysis_result['attack_type_id'],
                matched_rules=analysis_result['matched_rules'],
                recommended_actions=analysis_result['recommended_actions'],
                confidence_score=analysis_result['confidence_score'],
                explanation=analysis_result['explanation'],
                status='new',
                assigned_to=session.get('user_id')
            )
            db.session.add(incident)
        
        alert.status = 'processed'
        db.session.commit()
        
        flash('Alert re-analyzed successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error analyzing alert: {str(e)}', 'danger')
    
    return redirect(url_for('alerts.detail', alert_id=alert_id))
