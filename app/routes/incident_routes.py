"""
Incident Routes - HTTP endpoints for incident management and response tracking
"""
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.models.incident import Incident
from app.models.incident_history import IncidentHistory
from app.models.alert import Alert
from app.models.rule import Rule
from app.models.attack_type import AttackType
from extensions import db

incident_bp = Blueprint('incidents', __name__, url_prefix='/incidents')


def check_login():
    """Check if user is logged in"""
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return False
    return True


@incident_bp.route('/')
def index():
    """List all incidents - accessible by all logged-in users"""
    if not check_login():
        return redirect(url_for('auth.login'))
    
    # Get filter from query params
    status_filter = request.args.get('status', None)
    
    query = Incident.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    incidents = query.order_by(Incident.created_at.desc()).all()
    
    # Get counts for each status
    status_counts = {
        'all': Incident.query.count(),
        'new': Incident.query.filter_by(status='new').count(),
        'analyzing': Incident.query.filter_by(status='analyzing').count(),
        'pending': Incident.query.filter_by(status='pending').count(),
        'resolved': Incident.query.filter_by(status='resolved').count()
    }
    
    return render_template(
        'incidents/index.html',
        incidents=incidents,
        current_filter=status_filter,
        status_counts=status_counts
    )


@incident_bp.route('/<int:incident_id>')
def detail(incident_id: int):
    """View incident details with full analysis and action tracking"""
    if not check_login():
        return redirect(url_for('auth.login'))
    
    incident = Incident.query.get(incident_id)
    if not incident:
        flash('Incident not found.', 'danger')
        return redirect(url_for('incidents.index'))
    
    # Get related data
    alert = Alert.query.get(incident.alert_id)
    attack_type = AttackType.query.get(incident.attack_type_id) if incident.attack_type_id else None
    
    # Get matched rules
    matched_rules = []
    if incident.matched_rules:
        matched_rule_ids = incident.matched_rules
        matched_rules = Rule.query.filter(Rule.id.in_(matched_rule_ids)).all()
    
    # Get incident history
    history = IncidentHistory.query.filter_by(incident_id=incident_id)\
        .order_by(IncidentHistory.timestamp.desc()).all()
    
    return render_template(
        'incidents/detail.html',
        incident=incident,
        alert=alert,
        attack_type=attack_type,
        matched_rules=matched_rules,
        history=history
    )


@incident_bp.route('/<int:incident_id>/update-status', methods=['POST'])
def update_status(incident_id: int):
    """Update incident status - Analyst or Admin only"""
    if not check_login():
        return redirect(url_for('auth.login'))
    
    if session.get('user_role') not in ['admin', 'analyst']:
        flash('Only admins and analysts can update incident status.', 'danger')
        return redirect(url_for('incidents.detail', incident_id=incident_id))
    
    incident = Incident.query.get(incident_id)
    if not incident:
        flash('Incident not found.', 'danger')
        return redirect(url_for('incidents.index'))
    
    new_status = request.form.get('status')
    notes = request.form.get('notes', '')
    
    if new_status not in ['new', 'analyzing', 'pending', 'resolved']:
        flash('Invalid status value.', 'danger')
        return redirect(url_for('incidents.detail', incident_id=incident_id))
    
    try:
        old_status = incident.status
        incident.status = new_status
        incident.updated_at = datetime.utcnow()
        
        # If resolved, set resolved_at timestamp
        if new_status == 'resolved' and old_status != 'resolved':
            incident.resolved_at = datetime.utcnow()
        
        # Create history entry
        history_entry = IncidentHistory(
            incident_id=incident_id,
            action_taken=f'Status changed from {old_status} to {new_status}',
            notes=notes,
            performed_by=session.get('user_id')
        )
        
        db.session.add(history_entry)
        db.session.commit()
        
        flash(f'Incident status updated to {new_status}.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating status: {str(e)}', 'danger')
    
    return redirect(url_for('incidents.detail', incident_id=incident_id))


@incident_bp.route('/<int:incident_id>/add-action', methods=['POST'])
def add_action(incident_id: int):
    """Record an action taken on incident - Analyst or Admin only"""
    if not check_login():
        return redirect(url_for('auth.login'))
    
    if session.get('user_role') not in ['admin', 'analyst']:
        flash('Only admins and analysts can record actions.', 'danger')
        return redirect(url_for('incidents.detail', incident_id=incident_id))
    
    incident = Incident.query.get(incident_id)
    if not incident:
        flash('Incident not found.', 'danger')
        return redirect(url_for('incidents.index'))
    
    action_taken = request.form.get('action_taken', '').strip()
    notes = request.form.get('notes', '').strip()
    
    if not action_taken:
        flash('Action description is required.', 'warning')
        return redirect(url_for('incidents.detail', incident_id=incident_id))
    
    try:
        # Create history entry
        history_entry = IncidentHistory(
            incident_id=incident_id,
            action_taken=action_taken,
            notes=notes,
            performed_by=session.get('user_id')
        )
        
        db.session.add(history_entry)
        incident.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Action recorded successfully.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error recording action: {str(e)}', 'danger')
    
    return redirect(url_for('incidents.detail', incident_id=incident_id))


@incident_bp.route('/<int:incident_id>/assign', methods=['POST'])
def assign(incident_id: int):
    """Assign incident to a user - Analyst or Admin only"""
    if not check_login():
        return redirect(url_for('auth.login'))
    
    if session.get('user_role') not in ['admin', 'analyst']:
        flash('Only admins and analysts can assign incidents.', 'danger')
        return redirect(url_for('incidents.detail', incident_id=incident_id))
    
    incident = Incident.query.get(incident_id)
    if not incident:
        flash('Incident not found.', 'danger')
        return redirect(url_for('incidents.index'))
    
    assign_to_me = request.form.get('assign_to_me')
    
    try:
        if assign_to_me:
            incident.assigned_to = session.get('user_id')
            action_msg = 'assigned to themselves'
        else:
            incident.assigned_to = None
            action_msg = 'unassigned'
        
        # Create history entry
        history_entry = IncidentHistory(
            incident_id=incident_id,
            action_taken=f'Incident {action_msg}',
            notes='',
            performed_by=session.get('user_id')
        )
        
        db.session.add(history_entry)
        incident.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash(f'Incident {action_msg} successfully.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error assigning incident: {str(e)}', 'danger')
    
    return redirect(url_for('incidents.detail', incident_id=incident_id))
