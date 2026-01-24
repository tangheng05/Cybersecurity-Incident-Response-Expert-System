from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, IPAddress, Optional as OptionalValidator, Length, NumberRange


class AlertForm(FlaskForm):
    """Form for creating/submitting security alerts"""
    
    source_ip = StringField(
        'Source IP Address',
        validators=[DataRequired(), IPAddress(message='Invalid IP address')]
    )
    
    destination_ip = StringField(
        'Destination IP Address',
        validators=[OptionalValidator(), IPAddress(message='Invalid IP address')]
    )
    
    alert_type = SelectField(
        'Alert Type',
        choices=[],  # Will be populated dynamically
        validators=[DataRequired()]
    )
    
    severity = SelectField(
        'Severity Level',
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical')
        ],
        validators=[DataRequired()],
        default='medium'
    )
    
    # Brute Force Fields
    failed_attempts = IntegerField(
        'Failed Login Attempts',
        validators=[OptionalValidator(), NumberRange(min=0, max=1000)],
        render_kw={'placeholder': 'e.g., 5'}
    )
    
    target_service = StringField(
        'Target Service/Endpoint',
        validators=[OptionalValidator(), Length(max=100)],
        render_kw={'placeholder': 'e.g., ssh, /api/login'}
    )
    
    # DDoS Fields
    requests_per_second = IntegerField(
        'Requests Per Second',
        validators=[OptionalValidator(), NumberRange(min=0, max=1000000)],
        render_kw={'placeholder': 'e.g., 10000'}
    )
    
    time_window = IntegerField(
        'Time Window (seconds)',
        validators=[OptionalValidator(), NumberRange(min=1, max=86400)],
        render_kw={'placeholder': 'e.g., 300'}
    )
    
    description = TextAreaField(
        'Additional Details',
        validators=[OptionalValidator()],
        render_kw={'rows': 3, 'placeholder': 'Optional: Any additional information about this alert...'}
    )
    
    submit = SubmitField('Submit Alert for Analysis')
