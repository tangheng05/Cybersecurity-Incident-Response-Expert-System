import json
from flask import Blueprint, render_template, redirect, url_for, flash, abort, session
from app.forms.rule_forms import RuleForm, ConfirmDeleteRuleForm
from app.services import RuleService, AttackTypeService
from app.utils.decorators import login_required, role_required

rule_bp = Blueprint('rules', __name__, url_prefix='/rules')


@rule_bp.route('/')
@login_required
def index():
    rules = RuleService.get_all()
    attack_types = {at.id: at for at in AttackTypeService.get_all()}
    return render_template('rules/index.html', rules=rules, attack_types=attack_types)


@rule_bp.route('/<int:rule_id>')
@login_required
def detail(rule_id: int):
    rule = RuleService.get_by_id(rule_id)
    if rule is None:
        abort(404)
    return render_template('rules/detail.html', rule=rule)


@rule_bp.route('/create', methods=['GET', 'POST'])
@role_required('admin', 'analyst')
def create():
    form = RuleForm()
    # Populate attack type choices
    attack_types = AttackTypeService.get_all(active_only=True)
    form.attack_type_id.choices = [(at.id, at.name.replace('_', ' ').title()) for at in attack_types]
    
    if form.validate_on_submit():
        try:
            symbolic_conditions = [c.strip() for c in form.symbolic_conditions.data.strip().split('\n') if c.strip()]
            
            data = {
                'name': form.name.data,
                'attack_type_id': form.attack_type_id.data,
                'symbolic_conditions': symbolic_conditions,
                'conclusion': form.conclusion.data,
                'cf': form.cf.data,
                'priority': form.priority.data,
                'severity_score': form.severity_score.data,
                'is_active': form.is_active.data,
            }
            rule = RuleService.create(data)
            flash(f'Rule "{rule.name}" created successfully!', 'success')
            return redirect(url_for('rules.index'))
        except ValueError as e:
            flash(f'Validation error: {str(e)}', 'danger')
        except Exception as e:
            flash(f'Error creating rule: {str(e)}', 'danger')
    
    return render_template('rules/create.html', form=form)


@rule_bp.route('/<int:rule_id>/edit', methods=['GET', 'POST'])
@role_required('admin', 'analyst')
def edit(rule_id: int):
    rule = RuleService.get_by_id(rule_id)
    if rule is None:
        abort(404)
    
    form = RuleForm(obj=rule)
    attack_types = AttackTypeService.get_all(active_only=True)
    form.attack_type_id.choices = [(at.id, at.name.replace('_', ' ').title()) for at in attack_types]
    
    if form.validate_on_submit():
        try:
            symbolic_conditions = [c.strip() for c in form.symbolic_conditions.data.strip().split('\n') if c.strip()]
            
            data = {
                'name': form.name.data,
                'attack_type_id': form.attack_type_id.data,
                'symbolic_conditions': symbolic_conditions,
                'conclusion': form.conclusion.data,
                'cf': form.cf.data,
                'priority': form.priority.data,
                'severity_score': form.severity_score.data,
                'is_active': form.is_active.data,
            }
            RuleService.update(rule, data)
            flash(f'Rule "{rule.name}" updated successfully!', 'success')
            return redirect(url_for('rules.detail', rule_id=rule.id))
        except ValueError as e:
            flash(f'Validation error: {str(e)}', 'danger')
        except Exception as e:
            flash(f'Error updating rule: {str(e)}', 'danger')
    
    if not form.is_submitted():
        form.symbolic_conditions.data = '\n'.join(rule.symbolic_conditions or [])
        form.conclusion.data = rule.conclusion
        form.cf.data = rule.cf
    
    return render_template('rules/edit.html', form=form, rule=rule)


@rule_bp.route('/<int:rule_id>/delete', methods=['GET'])
@role_required('admin', 'analyst')
def delete_confirm(rule_id: int):
    rule = RuleService.get_by_id(rule_id)
    if rule is None:
        abort(404)
    
    form = ConfirmDeleteRuleForm()
    return render_template('rules/delete_confirm.html', rule=rule, form=form)


@rule_bp.route('/<int:rule_id>/delete', methods=['POST'])
@role_required('admin', 'analyst')
def delete(rule_id: int):
    rule = RuleService.get_by_id(rule_id)
    if rule is None:
        abort(404)
    
    rule_name = rule.name
    RuleService.delete(rule)
    flash(f'Rule "{rule_name}" deleted successfully!', 'success')
    return redirect(url_for('rules.index'))


@rule_bp.route('/<int:rule_id>/toggle', methods=['POST'])
@role_required('admin', 'analyst')
def toggle(rule_id: int):
    rule = RuleService.get_by_id(rule_id)
    if rule is None:
        abort(404)
    
    RuleService.toggle_active(rule)
    status = 'activated' if rule.is_active else 'deactivated'
    flash(f'Rule "{rule.name}" {status}!', 'success')
    return redirect(url_for('rules.index'))
