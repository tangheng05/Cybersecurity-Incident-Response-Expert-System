#!/usr/bin/env python3
"""
Script to create an admin user for the Cybersecurity Incident Response Expert System
Usage: python scripts/create_admin.py
"""
import sys
from getpass import getpass
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.models.user import User
from extensions import db


def create_admin():
    """Create an admin user interactively"""
    app = create_app()
    
    with app.app_context():
        print("=" * 50)
        print("Create Admin User")
        print("=" * 50)
        
        # Get user inputs
        username = input("Enter username: ").strip()
        if not username:
            print("Error: Username cannot be empty")
            sys.exit(1)
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"Error: Username '{username}' already exists")
            sys.exit(1)
        
        email = input("Enter email: ").strip()
        if not email:
            print("Error: Email cannot be empty")
            sys.exit(1)
        
        # Check if email already exists
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            print(f"Error: Email '{email}' already exists")
            sys.exit(1)
        
        full_name = input("Enter full name: ").strip()
        if not full_name:
            print("Error: Full name cannot be empty")
            sys.exit(1)
        
        # Get password
        password = getpass("Enter password: ")
        if not password:
            print("Error: Password cannot be empty")
            sys.exit(1)
        
        password_confirm = getpass("Confirm password: ")
        if password != password_confirm:
            print("Error: Passwords do not match")
            sys.exit(1)
        
        if len(password) < 6:
            print("Error: Password must be at least 6 characters long")
            sys.exit(1)
        
        # Create the admin user
        try:
            admin_user = User(
                username=username,
                email=email,
                full_name=full_name,
                role='admin',
                is_active=True
            )
            admin_user.set_password(password)
            
            db.session.add(admin_user)
            db.session.commit()
            
            print("\n" + "=" * 50)
            print("✓ Admin user created successfully!")
            print("=" * 50)
            print(f"Username: {username}")
            print(f"Email: {email}")
            print(f"Full Name: {full_name}")
            print(f"Role: admin")
            print("=" * 50)
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating admin user: {str(e)}")
            sys.exit(1)


def create_default_admin():
    """Create a default admin user with preset credentials"""
    app = create_app()
    
    with app.app_context():
        print("=" * 50)
        print("Create Default Admin User")
        print("=" * 50)
        
        # Default credentials
        username = "admin"
        email = "admin@example.com"
        full_name = "System Administrator"
        password = "admin123"
        
        # Check if admin already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"Admin user '{username}' already exists!")
            print("Use the interactive mode instead or delete the existing user first.")
            sys.exit(1)
        
        try:
            admin_user = User(
                username=username,
                email=email,
                full_name=full_name,
                role='admin',
                is_active=True
            )
            admin_user.set_password(password)
            
            db.session.add(admin_user)
            db.session.commit()
            
            print("\n✓ Default admin user created successfully!")
            print("=" * 50)
            print(f"Username: {username}")
            print(f"Email: {email}")
            print(f"Password: {password}")
            print(f"Full Name: {full_name}")
            print(f"Role: admin")
            print("=" * 50)
            print("\n⚠️  WARNING: Please change the default password after first login!")
            print("=" * 50)
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating default admin user: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    print("\nCybersecurity Incident Response Expert System")
    print("Admin User Creation Tool\n")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--default":
        create_default_admin()
    else:
        print("Options:")
        print("1. Create admin interactively")
        print("2. Create default admin (username: admin, password: admin123)")
        print()
        choice = input("Choose option (1 or 2): ").strip()
        
        if choice == "1":
            create_admin()
        elif choice == "2":
            create_default_admin()
        else:
            print("Invalid choice. Exiting.")
            sys.exit(1)
