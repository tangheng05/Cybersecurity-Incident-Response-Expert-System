from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.models import User
from app.utils.decorators import admin_required
from extensions import db

role_bp = Blueprint('roles', __name__, url_prefix='/roles')


@role_bp.route('/')
@admin_required
def index():
    """Display all roles with their descriptions and user counts"""
    # Define role information
    roles = [
        {
            'name': 'admin',
            'display_name': 'Administrator',
            'description': 'Full system access with all permissions',
            'permissions': [
                'Manage users and roles',
                'Create/edit/delete attack types',
                'Create/edit/delete security rules',
                'View and manage all alerts',
                'View and manage all incidents',
                'Access all reports and analytics',
                'System configuration'
            ],
            'badge_color': 'danger'
        },
        {
            'name': 'analyst',
            'display_name': 'Security Analyst',
            'description': 'Manage security content and analyze threats',
            'permissions': [
                'Create/edit/delete attack types',
                'Create/edit/delete security rules',
                'View and manage all alerts',
                'View and manage all incidents',
                'Access reports and analytics'
            ],
            'badge_color': 'warning'
        },
        {
            'name': 'viewer',
            'display_name': 'Operator / Viewer',
            'description': 'Read-only access to security data',
            'permissions': [
                'View alerts',
                'View incidents',
                'View attack types',
                'View security rules',
                'View basic reports'
            ],
            'badge_color': 'info'
        }
    ]
    
    # Get user counts for each role
    for role in roles:
        role['user_count'] = User.query.filter_by(role=role['name']).count()
        role['users'] = User.query.filter_by(role=role['name']).all()
    
    return render_template('roles/index.html', roles=roles)


@role_bp.route('/<role_name>')
@admin_required
def detail(role_name):
    """Display detailed information about a specific role"""
    # Define role information
    role_info = {
        'admin': {
            'name': 'admin',
            'display_name': 'Administrator',
            'description': 'Full system access with all permissions',
            'permissions': [
                'Manage users and roles',
                'Create/edit/delete attack types',
                'Create/edit/delete security rules',
                'View and manage all alerts',
                'View and manage all incidents',
                'Access all reports and analytics',
                'System configuration'
            ],
            'badge_color': 'danger'
        },
        'analyst': {
            'name': 'analyst',
            'display_name': 'Security Analyst',
            'description': 'Manage security content and analyze threats',
            'permissions': [
                'Create/edit/delete attack types',
                'Create/edit/delete security rules',
                'View and manage all alerts',
                'View and manage all incidents',
                'Access reports and analytics'
            ],
            'badge_color': 'warning'
        },
        'viewer': {
            'name': 'viewer',
            'display_name': 'Operator / Viewer',
            'description': 'Read-only access to security data',
            'permissions': [
                'View alerts',
                'View incidents',
                'View attack types',
                'View security rules',
                'View basic reports'
            ],
            'badge_color': 'info'
        }
    }
    
    if role_name not in role_info:
        flash('Role not found.', 'danger')
        return redirect(url_for('roles.index'))
    
    role = role_info[role_name]
    role['users'] = User.query.filter_by(role=role_name).all()
    role['user_count'] = len(role['users'])
    
    return render_template('roles/detail.html', role=role)
