import json
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError


class RuleForm(FlaskForm):
    name = StringField(
        'Rule Name',
        validators=[DataRequired(), Length(min=5, max=200)],
        render_kw={'placeholder': 'e.g., Brute Force - Multiple Failed Logins'}
    )
    
    attack_type_id = SelectField(
        'Attack Type',
        coerce=int,
        validators=[DataRequired()]
    )
    
    conditions = TextAreaField(
        'Conditions (JSON)',
        validators=[DataRequired()],
        render_kw={
            'rows': 8,
            'placeholder': '{\n  "failed_attempts": ">= 5",\n  "time_window": "5 minutes",\n  "same_ip": true\n}'
        }
    )
    
    actions = TextAreaField(
        'Actions (JSON Array)',
        validators=[DataRequired()],
        render_kw={
            'rows': 5,
            'placeholder': '["block_ip", "alert_admin", "log_incident"]'
        }
    )
    
    priority = SelectField(
        'Priority',
        choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')],
        validators=[DataRequired()]
    )
    
    severity_score = IntegerField(
        'Severity Score (1-10)',
        validators=[DataRequired(), NumberRange(min=1, max=10)],
        default=5
    )
    
    match_threshold = IntegerField(
        'Match Threshold (%)',
        validators=[DataRequired(), NumberRange(min=1, max=100)],
        default=70,
        render_kw={'placeholder': '70'}
    )
    
    is_active = BooleanField('Active', default=True)
    
    submit = SubmitField('Save Rule')
    
    def validate_conditions(self, field):
        """Validate that conditions is valid JSON"""
        try:
            json.loads(field.data)
        except json.JSONDecodeError as e:
            raise ValidationError(f'Invalid JSON format: {str(e)}')
    
    def validate_actions(self, field):
        """Validate that actions is valid JSON array"""
        try:
            data = json.loads(field.data)
            if not isinstance(data, list):
                raise ValidationError('Actions must be a JSON array')
            if not all(isinstance(item, str) for item in data):
                raise ValidationError('All actions must be strings')
        except json.JSONDecodeError as e:
            raise ValidationError(f'Invalid JSON format: {str(e)}')


class ConfirmDeleteRuleForm(FlaskForm):
    submit = SubmitField('Confirm Delete')
