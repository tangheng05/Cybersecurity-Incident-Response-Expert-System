from functools import wraps
from flask import session, redirect, url_for, flash, abort


def login_required(f):
    """Decorator to require user to be logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require user to be admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Get fresh user data from database to ensure role is current
        from app.models.user import User
        user = User.query.get(session.get('user_id'))
        
        if not user or not user.is_active:
            session.clear()
            flash('Your account is no longer active. Please contact an administrator.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Update session with current role
        if session.get('user_role') != user.role:
            session['user_role'] = user.role
        
        if user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    """Decorator to require specific role(s)"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('user_id'):
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            
            # Get fresh user data from database to ensure role is current
            from app.models.user import User
            user = User.query.get(session.get('user_id'))
            
            if not user or not user.is_active:
                session.clear()
                flash('Your account is no longer active. Please contact an administrator.', 'warning')
                return redirect(url_for('auth.login'))
            
            # Update session with current role
            if session.get('user_role') != user.role:
                session['user_role'] = user.role
            
            if user.role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
