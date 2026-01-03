from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class AttackTypeForm(FlaskForm):
    """Form for creating/editing attack types"""
    
    name = StringField('Attack Type Name', 
                      validators=[
                          DataRequired(message='Attack type name is required'),
                          Length(min=3, max=100, message='Name must be between 3 and 100 characters')
                      ])
    
    description = TextAreaField('Description',
                               validators=[
                                   DataRequired(message='Description is required'),
                                   Length(min=10, max=500, message='Description must be between 10 and 500 characters')
                               ])
    
    severity_level = IntegerField('Severity Level (1-10)',
                                 validators=[
                                     DataRequired(message='Severity level is required'),
                                     NumberRange(min=1, max=10, message='Severity must be between 1 and 10')
                                 ],
                                 default=5)
    
    is_active = BooleanField('Active', default=True)
    
    submit = SubmitField('Save Attack Type')
