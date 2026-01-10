import re
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from app.models import User
from extensions import db


# ----- helpers -----

def strong_password(form, field):
    """Require: min 8 chars, upper, lower, digit, special."""
    password = field.data or ""
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter.")

    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")

    if not re.search(r"[0-9]", password):
        raise ValidationError("Password must contain at least one digit.")

    if not re.search(r"[!@#$%^&*(),.?\"\':;{}|<>\/\\\-_+=]", password):
        raise ValidationError("Password must contain at least one special character.")


# ----- create form (password required) -----

class UserCreateForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=80)],
        render_kw={"placeholder": ""},
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)],
        render_kw={"placeholder": "Enter email"},
    )
    full_name = StringField(
        "Full name",
        validators=[DataRequired(), Length(min=1, max=120)],
        render_kw={"placeholder": "Enter full name"},
    )
    role = SelectField(
        "Role",
        choices=[
            ('admin', 'Administrator'),
            ('analyst', 'Security Analyst'),
            ('viewer', 'Viewer')
        ],
        validators=[DataRequired()],
    )
    is_active = BooleanField("Active", default=True)

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            strong_password,
        ],
        render_kw={"placeholder": "Strong password"},
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
        render_kw={"placeholder": "Confirm password"},
    )

    submit = SubmitField("Save")

    # ---- server-side uniqueness checks ----

    def validate_username(self, field):
        exists = db.session.scalar(
            db.select(User).filter(User.username == field.data)
        )
        if exists:
            raise ValidationError("This username is already taken.")

    def validate_email(self, field):
        exists = db.session.scalar(
            db.select(User).filter(User.email == field.data)
        )
        if exists:
            raise ValidationError("This email is already registered.")


# ----- edit form (password optional) -----

class UserEditForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=80)],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)],
    )
    full_name = StringField(
        "Full name",
        validators=[DataRequired(), Length(min=1, max=120)],
    )
    role = SelectField(
        "Role",
        choices=[
            ('admin', 'Administrator'),
            ('analyst', 'Security Analyst'),
            ('viewer', 'Viewer')
        ],
        validators=[DataRequired()],
    )
    is_active = BooleanField("Active")

    # optional password - only change if filled
    password = PasswordField(
        "New password (leave blank to keep current)",
        validators=[],
        render_kw={"placeholder": "New strong password (optional)"},
    )
    confirm_password = PasswordField(
        "Confirm new password",
        validators=[EqualTo("password", message="Passwords must match.")],
    )

    submit = SubmitField("Update")

    def __init__(self, original_user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_user = original_user

    def validate_username(self, field):
        q = db.select(User).filter(User.username == field.data, User.id != self.original_user.id)
        exists = db.session.scalar(q)
        if exists:
            raise ValidationError("This username is already taken.")

    def validate_email(self, field):
        q = db.select(User).filter(User.email == field.data, User.id != self.original_user.id)
        exists = db.session.scalar(q)
        if exists:
            raise ValidationError("This email is already registered.")


class ConfirmDeleteForm(FlaskForm):
    submit = SubmitField("Confirm Delete")

