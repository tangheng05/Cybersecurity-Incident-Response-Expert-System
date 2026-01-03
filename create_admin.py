"""
Script to create an initial admin user for the Cybersecurity IRS system.
Run this after the first application startup to create the admin account.
"""
from app import create_app
from app.models import User
from extensions import db

app = create_app()

with app.app_context():
    # Check if admin already exists
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print("Admin user already exists!")
    else:
        # Create admin user
        admin = User(
            username='admin',
            email='admin@cybersec.local',
            full_name='System Administrator',
            role='admin',
            is_active=True
        )
        admin.set_password('Admin@123')
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Admin user created successfully!")
        print("Username: admin")
        print("Password: Admin@123")
        print("\n⚠️  Please change the password after first login!")
