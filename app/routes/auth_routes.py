from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from datetime import datetime
from app.forms.auth_forms import LoginForm, RegisterForm
from app.forms.user_forms import UserProfileForm
from app.models import User
from app.utils.decorators import login_required
from extensions import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect to dashboard if already logged in
    if session.get('user_id'):
        return redirect(url_for('dashboard.index'))
    
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
            session['user_role'] = user.role  # Changed from 'role' to 'user_role'
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Redirect to dashboard if already logged in
    if session.get('user_id'):
        return redirect(url_for('dashboard.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Create new user with 'viewer' role (operator/normal user)
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            role='viewer',  # Default role for self-registered users
            is_active=True
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created successfully! You can now log in as {user.username}.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Allow users to edit their own profile"""
    user = User.query.get(session.get('user_id'))
    if not user:
        session.clear()
        flash('User not found. Please log in again.', 'danger')
        return redirect(url_for('auth.login'))
    
    form = UserProfileForm(original_user=user, obj=user)
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.full_name = form.full_name.data
        
        # Update password if provided
        if form.password.data:
            user.set_password(form.password.data)
        
        db.session.commit()
        
        # Update session with new username
        session['username'] = user.username
        
        flash('Your profile has been updated successfully!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/profile.html', form=form, user=user)


@auth_bp.route('/logout')
def logout():
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
