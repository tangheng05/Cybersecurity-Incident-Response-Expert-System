"""
Seed the database with initial attack types and security rules.
Run this after creating the admin user.
"""
from app import create_app
from app.models import AttackType, Rule
from extensions import db

app = create_app()

with app.app_context():
    # Create Attack Types
    print("Creating attack types...")
    
    brute_force = AttackType.query.filter_by(name='brute_force').first()
    if not brute_force:
        brute_force = AttackType(
            name='brute_force',
            description='Automated attempts to guess credentials by trying multiple username/password combinations',
            severity_level=8,
            is_active=True
        )
        db.session.add(brute_force)
    
    ddos = AttackType.query.filter_by(name='ddos').first()
    if not ddos:
        ddos = AttackType(
            name='ddos',
            description='Distributed Denial of Service - overwhelming a system with traffic to make it unavailable',
            severity_level=9,
            is_active=True
        )
        db.session.add(ddos)
    
    db.session.commit()
    print(f"✅ Attack types created: {brute_force.name}, {ddos.name}")
    
    # Create Brute Force Rules
    print("\nCreating Brute Force rules...")
    
    brute_force_rules = [
        {
            'name': 'Brute Force - Multiple Failed Logins (Same IP)',
            'attack_type_id': brute_force.id,
            'conditions': {
                'failed_attempts': '>= 5',
                'time_window': '5 minutes',
                'same_ip': True
            },
            'actions': ['block_ip', 'alert_admin', 'log_incident', 'require_captcha'],
            'priority': 'high',
            'severity_score': 9
        },
        {
            'name': 'Brute Force - Failed Logins Across Multiple Accounts',
            'attack_type_id': brute_force.id,
            'conditions': {
                'failed_attempts': '>= 10',
                'time_window': '10 minutes',
                'unique_usernames': '>= 3',
                'same_ip': True
            },
            'actions': ['block_ip', 'alert_admin', 'log_incident'],
            'priority': 'high',
            'severity_score': 8
        },
        {
            'name': 'Brute Force - Login Attempts Outside Business Hours',
            'attack_type_id': brute_force.id,
            'conditions': {
                'failed_attempts': '>= 3',
                'time_window': '15 minutes',
                'time_of_day': 'outside_business_hours'
            },
            'actions': ['alert_admin', 'log_incident', 'increase_monitoring'],
            'priority': 'medium',
            'severity_score': 7
        },
        {
            'name': 'Brute Force - Geographic Anomaly Detection',
            'attack_type_id': brute_force.id,
            'conditions': {
                'failed_attempts': '>= 3',
                'time_window': '10 minutes',
                'geographic_distance': '> 1000 km',
                'time_between_attempts': '< 5 minutes'
            },
            'actions': ['alert_admin', 'require_mfa', 'log_incident'],
            'priority': 'high',
            'severity_score': 8
        },
        {
            'name': 'Brute Force - Rapid Sequential Attempts',
            'attack_type_id': brute_force.id,
            'conditions': {
                'failed_attempts': '>= 20',
                'time_window': '1 minute',
                'same_username': True
            },
            'actions': ['block_ip', 'lock_account', 'alert_admin', 'log_incident'],
            'priority': 'high',
            'severity_score': 9
        }
    ]
    
    # Create DDoS Rules
    print("Creating DDoS rules...")
    
    ddos_rules = [
        {
            'name': 'DDoS - High Traffic Volume from Single IP',
            'attack_type_id': ddos.id,
            'conditions': {
                'requests_per_second': '>= 100',
                'time_window': '1 minute',
                'same_ip': True
            },
            'actions': ['block_ip', 'rate_limit', 'alert_admin', 'log_incident'],
            'priority': 'high',
            'severity_score': 9
        },
        {
            'name': 'DDoS - Distributed High Volume Attack',
            'attack_type_id': ddos.id,
            'conditions': {
                'total_requests_per_second': '>= 1000',
                'unique_source_ips': '>= 50',
                'time_window': '2 minutes'
            },
            'actions': ['enable_ddos_mitigation', 'alert_admin', 'log_incident', 'contact_isp'],
            'priority': 'high',
            'severity_score': 10
        },
        {
            'name': 'DDoS - SYN Flood Detection',
            'attack_type_id': ddos.id,
            'conditions': {
                'syn_packets': '>= 500',
                'time_window': '1 minute',
                'incomplete_connections': '>= 80%'
            },
            'actions': ['enable_syn_cookies', 'block_suspicious_ips', 'alert_admin', 'log_incident'],
            'priority': 'high',
            'severity_score': 9
        },
        {
            'name': 'DDoS - UDP Flood Detection',
            'attack_type_id': ddos.id,
            'conditions': {
                'udp_packets_per_second': '>= 200',
                'time_window': '1 minute',
                'destination_port': 'random'
            },
            'actions': ['filter_udp_traffic', 'alert_admin', 'log_incident'],
            'priority': 'high',
            'severity_score': 8
        },
        {
            'name': 'DDoS - HTTP GET/POST Flood',
            'attack_type_id': ddos.id,
            'conditions': {
                'http_requests_per_second': '>= 500',
                'time_window': '1 minute',
                'unique_user_agents': '< 5'
            },
            'actions': ['enable_challenge_response', 'rate_limit', 'alert_admin', 'log_incident'],
            'priority': 'high',
            'severity_score': 9
        },
        {
            'name': 'DDoS - Slowloris Attack Detection',
            'attack_type_id': ddos.id,
            'conditions': {
                'slow_connections': '>= 100',
                'connection_duration': '> 10 minutes',
                'incomplete_requests': True
            },
            'actions': ['timeout_slow_connections', 'block_ip', 'alert_admin', 'log_incident'],
            'priority': 'medium',
            'severity_score': 7
        }
    ]
    
    # Insert all rules
    all_rules = brute_force_rules + ddos_rules
    created_count = 0
    
    for rule_data in all_rules:
        existing = Rule.query.filter_by(name=rule_data['name']).first()
        if not existing:
            rule = Rule(**rule_data)
            db.session.add(rule)
            created_count += 1
            print(f"  ✅ {rule_data['name']}")
        else:
            print(f"  ⏭️  {rule_data['name']} (already exists)")
    
    db.session.commit()
    
    print(f"\n✅ Seeding complete!")
    print(f"   - {created_count} new rules created")
    print(f"   - Total rules in database: {Rule.query.count()}")
    print(f"   - Brute Force rules: {Rule.query.filter_by(attack_type_id=brute_force.id).count()}")
    print(f"   - DDoS rules: {Rule.query.filter_by(attack_type_id=ddos.id).count()}")
