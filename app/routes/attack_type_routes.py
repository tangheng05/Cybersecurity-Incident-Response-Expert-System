from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.models.attack_type import AttackType
from app.forms.attack_type_forms import AttackTypeForm
from app.services.attack_type_service import AttackTypeService
from app.utils.decorators import login_required, role_required
from extensions import db

attack_type_bp = Blueprint('attack_type', __name__, url_prefix='/attack-types')


@attack_type_bp.route('/')
@login_required
def index():
    """List all attack types - accessible by all logged-in users"""
    
    attack_types = AttackTypeService.get_all()
    return render_template('attack_types/index.html', attack_types=attack_types)


@attack_type_bp.route('/<int:id>')
@login_required
def detail(id):
    """View attack type details - accessible by all logged-in users"""
    attack_type = AttackTypeService.get_by_id(id)
    if not attack_type:
        flash('Attack type not found.', 'danger')
        return redirect(url_for('attack_type.index'))
    
    return render_template('attack_types/detail.html', attack_type=attack_type)


@attack_type_bp.route('/create', methods=['GET', 'POST'])
@role_required('admin', 'analyst')
def create():
    """Create new attack type - Security Analyst and Admin only"""
    form = AttackTypeForm()
    
    if form.validate_on_submit():
        attack_type = AttackTypeService.create(
            name=form.name.data,
            description=form.description.data,
            severity_level=form.severity_level.data,
            is_active=form.is_active.data
        )
        
        flash(f'Attack type "{attack_type.name}" created successfully!', 'success')
        return redirect(url_for('attack_type.detail', id=attack_type.id))
    
    return render_template('attack_types/create.html', form=form)


@attack_type_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@role_required('admin', 'analyst')
def edit(id):
    """Edit attack type - Security Analyst and Admin only"""
    attack_type = AttackTypeService.get_by_id(id)
    if not attack_type:
        flash('Attack type not found.', 'danger')
        return redirect(url_for('attack_type.index'))
    
    form = AttackTypeForm(obj=attack_type)
    
    if form.validate_on_submit():
        updated_attack_type = AttackTypeService.update(
            id,
            name=form.name.data,
            description=form.description.data,
            severity_level=form.severity_level.data,
            is_active=form.is_active.data
        )
        
        flash(f'Attack type "{updated_attack_type.name}" updated successfully!', 'success')
        return redirect(url_for('attack_type.detail', id=updated_attack_type.id))
    
    return render_template('attack_types/edit.html', form=form, attack_type=attack_type)


@attack_type_bp.route('/<int:id>/toggle-status', methods=['POST'])
@role_required('admin', 'analyst')
def toggle_status(id):
    """Toggle attack type active status - Security Analyst and Admin only"""
    attack_type = AttackTypeService.toggle_active(id)
    if attack_type:
        status = 'activated' if attack_type.is_active else 'deactivated'
        flash(f'Attack type "{attack_type.name}" {status} successfully!', 'success')
    else:
        flash('Attack type not found.', 'danger')
    
    return redirect(url_for('attack_type.index'))


@attack_type_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@role_required('admin', 'analyst')
def delete(id):
    """Delete attack type - Admin and Analyst"""
    attack_type = AttackTypeService.get_by_id(id)
    if not attack_type:
        flash('Attack type not found.', 'danger')
        return redirect(url_for('attack_type.index'))
    
    if request.method == 'POST':
        # Check if attack type has associated rules
        if attack_type.rules:
            flash(f'Cannot delete "{attack_type.name}" - it has {len(attack_type.rules)} associated rules.', 'danger')
            return redirect(url_for('attack_type.detail', id=id))
        
        AttackTypeService.delete(id)
        flash(f'Attack type "{attack_type.name}" deleted successfully!', 'success')
        return redirect(url_for('attack_type.index'))
    
    return render_template('attack_types/delete_confirm.html', attack_type=attack_type)
