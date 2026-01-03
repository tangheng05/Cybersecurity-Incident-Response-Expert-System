from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from datetime import datetime
from app.forms.auth_forms import LoginForm
from app.models import User
from extensions import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Your account is inactive. Please contact an administrator.', 'danger')
                return redirect(url_for('auth.login'))
            
            # Store user info in session
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
