import json
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, FloatField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError


class RuleForm(FlaskForm):
    name = StringField(
        'Rule Name',
        validators=[DataRequired(), Length(min=5, max=200)],
        render_kw={'placeholder': 'e.g., High Failed Attempts with Short Window'}
    )
    
    attack_type_id = SelectField(
        'Attack Type',
        coerce=int,
        validators=[DataRequired()]
    )
    
    symbolic_conditions = TextAreaField(
        'Symbolic Conditions (one per line)',
        validators=[DataRequired()],
        render_kw={
            'rows': 6,
            'placeholder': 'high_failed_attempts\nshort_timespan\nadmin_target'
        }
    )
    
    conclusion = StringField(
        'Conclusion',
        validators=[DataRequired(), Length(max=100)],
        render_kw={'placeholder': 'e.g., brute_force_attack'}
    )
    
    cf = FloatField(
        'Certainty Factor (0.0 - 1.0)',
        validators=[DataRequired(), NumberRange(min=0.0, max=1.0)],
        default=0.8,
        render_kw={'step': '0.01', 'placeholder': '0.85'}
    )
    
    is_active = BooleanField('Active', default=True)
    
    submit = SubmitField('Save Rule')
    
    def validate_symbolic_conditions(self, field):
        conditions = [c.strip() for c in field.data.strip().split('\n') if c.strip()]
        if len(conditions) == 0:
            raise ValidationError('At least one symbolic condition is required')


class ConfirmDeleteRuleForm(FlaskForm):
    submit = SubmitField('Confirm Delete')
