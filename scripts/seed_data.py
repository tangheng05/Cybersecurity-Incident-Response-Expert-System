#!/usr/bin/env python3
"""
Seed script to populate the database with default attack types and security rules
Usage: python scripts/seed_data.py
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.models.attack_type import AttackType
from app.models.rule import Rule
from extensions import db


def seed_attack_types():
    """Seed default attack types"""
    attack_types_data = [
        {
            'name': 'brute_force',
            'description': 'Brute force attack attempting multiple login combinations',
            'severity_level': 8,
            'is_active': True
        },
        {
            'name': 'ddos',
            'description': 'Distributed Denial of Service attack overwhelming system resources',
            'severity_level': 9,
            'is_active': True
        },
        {
            'name': 'sql_injection',
            'description': 'SQL injection attack attempting to manipulate database queries',
            'severity_level': 10,
            'is_active': True
        },
        {
            'name': 'xss',
            'description': 'Cross-Site Scripting attack injecting malicious scripts',
            'severity_level': 7,
            'is_active': True
        },
        {
            'name': 'malware',
            'description': 'Malware infection detected on system',
            'severity_level': 10,
            'is_active': True
        },
        {
            'name': 'phishing',
            'description': 'Phishing attempt to steal credentials or sensitive information',
            'severity_level': 6,
            'is_active': True
        },
        {
            'name': 'port_scan',
            'description': 'Port scanning activity detecting open ports and services',
            'severity_level': 5,
            'is_active': True
        },
        {
            'name': 'unauthorized_access',
            'description': 'Unauthorized access attempt to restricted resources',
            'severity_level': 8,
            'is_active': True
        },
        {
            'name': 'data_exfiltration',
            'description': 'Suspicious data transfer indicating possible data theft',
            'severity_level': 10,
            'is_active': True
        },
        {
            'name': 'privilege_escalation',
            'description': 'Attempt to gain elevated privileges in the system',
            'severity_level': 9,
            'is_active': True
        }
    ]
    
    created_count = 0
    skipped_count = 0
    
    for data in attack_types_data:
        existing = AttackType.query.filter_by(name=data['name']).first()
        if existing:
            print(f"  ⊘ Attack type '{data['name']}' already exists, skipping...")
            skipped_count += 1
            continue
        
        attack_type = AttackType(**data)
        db.session.add(attack_type)
        created_count += 1
        print(f"  ✓ Created attack type: {data['name']}")
    
    db.session.commit()
    return created_count, skipped_count


def seed_rules():
    """Seed default security rules"""
    rules_data = [
        {
            'name': 'Multiple Failed Login Attempts',
            'attack_type': 'brute_force',
            'conditions': {
                'failed_login_count': {'operator': '>', 'value': 5},
                'time_window': {'value': 300, 'unit': 'seconds'}
            },
            'actions': ['block_ip', 'alert_admin', 'log_incident'],
            'priority': 'high',
            'severity_score': 8,
            'is_active': True
        },
        {
            'name': 'High Volume Traffic from Single Source',
            'attack_type': 'ddos',
            'conditions': {
                'request_count': {'operator': '>', 'value': 1000},
                'time_window': {'value': 60, 'unit': 'seconds'}
            },
            'actions': ['rate_limit', 'block_ip', 'alert_admin'],
            'priority': 'high',
            'severity_score': 9,
            'is_active': True
        },
        {
            'name': 'SQL Injection Pattern Detected',
            'attack_type': 'sql_injection',
            'conditions': {
                'request_contains': {'patterns': ['UNION SELECT', 'OR 1=1', 'DROP TABLE', '--', 'EXEC']},
                'method': {'value': 'POST'}
            },
            'actions': ['block_request', 'block_ip', 'alert_admin', 'log_incident'],
            'priority': 'high',
            'severity_score': 10,
            'is_active': True
        },
        {
            'name': 'XSS Script Tag Detection',
            'attack_type': 'xss',
            'conditions': {
                'request_contains': {'patterns': ['<script>', 'javascript:', 'onerror=', 'onload=']},
            },
            'actions': ['sanitize_input', 'block_request', 'alert_admin'],
            'priority': 'medium',
            'severity_score': 7,
            'is_active': True
        },
        {
            'name': 'Suspicious File Upload',
            'attack_type': 'malware',
            'conditions': {
                'file_extension': {'matches': ['.exe', '.bat', '.cmd', '.sh', '.ps1']},
                'upload_detected': True
            },
            'actions': ['block_upload', 'quarantine_file', 'alert_admin', 'scan_file'],
            'priority': 'high',
            'severity_score': 9,
            'is_active': True
        },
        {
            'name': 'Port Scan Detection',
            'attack_type': 'port_scan',
            'conditions': {
                'unique_ports_accessed': {'operator': '>', 'value': 20},
                'time_window': {'value': 60, 'unit': 'seconds'}
            },
            'actions': ['block_ip', 'alert_admin', 'log_incident'],
            'priority': 'medium',
            'severity_score': 5,
            'is_active': True
        },
        {
            'name': 'Unauthorized Admin Access Attempt',
            'attack_type': 'unauthorized_access',
            'conditions': {
                'endpoint_accessed': {'matches': ['/admin', '/config', '/system']},
                'user_role': {'operator': '!=', 'value': 'admin'}
            },
            'actions': ['block_access', 'alert_admin', 'log_incident'],
            'priority': 'high',
            'severity_score': 8,
            'is_active': True
        },
        {
            'name': 'Large Data Transfer',
            'attack_type': 'data_exfiltration',
            'conditions': {
                'data_transfer_size': {'operator': '>', 'value': 104857600},  # 100MB
                'time_window': {'value': 300, 'unit': 'seconds'}
            },
            'actions': ['rate_limit', 'alert_admin', 'log_incident', 'monitor_connection'],
            'priority': 'high',
            'severity_score': 10,
            'is_active': True
        },
        {
            'name': 'Privilege Escalation Attempt',
            'attack_type': 'privilege_escalation',
            'conditions': {
                'permission_change_requested': True,
                'user_role': {'operator': '!=', 'value': 'admin'}
            },
            'actions': ['block_action', 'alert_admin', 'log_incident', 'lock_account'],
            'priority': 'high',
            'severity_score': 9,
            'is_active': True
        },
        {
            'name': 'Suspicious Email Pattern',
            'attack_type': 'phishing',
            'conditions': {
                'email_contains': {'patterns': ['verify your account', 'urgent action required', 'click here immediately']},
                'suspicious_links': True
            },
            'actions': ['quarantine_email', 'alert_user', 'log_incident'],
            'priority': 'medium',
            'severity_score': 6,
            'is_active': True
        }
    ]
    
    created_count = 0
    skipped_count = 0
    
    for data in rules_data:
        # Find the attack type
        attack_type_name = data.pop('attack_type')
        attack_type = AttackType.query.filter_by(name=attack_type_name).first()
        
        if not attack_type:
            print(f"  ⚠ Attack type '{attack_type_name}' not found, skipping rule '{data['name']}'")
            skipped_count += 1
            continue
        
        # Check if rule already exists
        existing = Rule.query.filter_by(name=data['name']).first()
        if existing:
            print(f"  ⊘ Rule '{data['name']}' already exists, skipping...")
            skipped_count += 1
            continue
        
        rule = Rule(
            attack_type_id=attack_type.id,
            **data
        )
        db.session.add(rule)
        created_count += 1
        print(f"  ✓ Created rule: {data['name']}")
    
    db.session.commit()
    return created_count, skipped_count


def main():
    """Main seeding function"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "=" * 70)
        print("Cybersecurity Incident Response Expert System - Database Seeding")
        print("=" * 70 + "\n")
        
        try:
            # Seed attack types
            print("Seeding Attack Types...")
            attack_created, attack_skipped = seed_attack_types()
            print(f"\n  Summary: {attack_created} created, {attack_skipped} skipped\n")
            
            # Seed rules
            print("Seeding Security Rules...")
            rule_created, rule_skipped = seed_rules()
            print(f"\n  Summary: {rule_created} created, {rule_skipped} skipped\n")
            
            print("=" * 70)
            print("✓ Database seeding completed successfully!")
            print("=" * 70)
            print(f"\nTotal Results:")
            print(f"  - Attack Types: {attack_created} created, {attack_skipped} skipped")
            print(f"  - Security Rules: {rule_created} created, {rule_skipped} skipped")
            print("=" * 70 + "\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ Error during seeding: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    main()
