from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, IPAddress, Optional as OptionalValidator, Length
import json


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
    
    alert_type = StringField(
        'Alert Type',
        validators=[DataRequired(), Length(min=3, max=50)],
        default='manual_submission'
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
    
    raw_data = TextAreaField(
        'Alert Data (JSON)',
        validators=[DataRequired()],
        render_kw={'rows': 10, 'placeholder': '{\n  "failed_attempts": 6,\n  "time_window": "5 minutes"\n}'}
    )
    
    submit = SubmitField('Submit Alert for Analysis')
    
    def validate_raw_data(self, field):
        """Validate that raw_data is valid JSON"""
        try:
            json.loads(field.data)
        except json.JSONDecodeError as e:
            raise ValueError(f'Invalid JSON format: {str(e)}')
