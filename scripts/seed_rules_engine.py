"""
Seed Rules for Forward-Chaining Inference Engine
Converts rules to symbolic format with Certainty Factors
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.models.attack_type import AttackType
from app.models.rule import Rule
from extensions import db


def seed_rules_new_engine():
    """Seed rules for forward-chaining inference engine"""
    
    rules_data = [
        {
            'name': 'High Failed Attempts with Short Window',
            'attack_type': 'brute_force',
            'symbolic_conditions': ['high_failed_attempts', 'short_timespan'],
            'conclusion': 'brute_force_attack',
            'cf': 0.85,
            'priority': 'high',
            'severity_score': 8
        },
        {
            'name': 'Very High Failed Attempts Rapid',
            'attack_type': 'brute_force',
            'symbolic_conditions': ['very_high_failed_attempts', 'very_short_timespan'],
            'conclusion': 'brute_force_attack',
            'cf': 0.92,
            'priority': 'high',
            'severity_score': 9
        },
        {
            'name': 'Admin Account Targeted Brute Force',
            'attack_type': 'brute_force',
            'symbolic_conditions': ['high_failed_attempts', 'admin_target'],
            'conclusion': 'brute_force_attack',
            'cf': 0.88,
            'priority': 'high',
            'severity_score': 9
        },
        {
            'name': 'SSH Brute Force Pattern',
            'attack_type': 'brute_force',
            'symbolic_conditions': ['ssh_service', 'high_failed_attempts', 'short_timespan'],
            'conclusion': 'brute_force_attack',
            'cf': 0.90,
            'priority': 'high',
            'severity_score': 8
        },
        {
            'name': 'Credential Stuffing Detected',
            'attack_type': 'brute_force',
            'symbolic_conditions': ['high_failed_attempts', 'repeat_offender'],
            'conclusion': 'credential_stuffing',
            'cf': 0.87,
            'priority': 'high',
            'severity_score': 8
        },
        {
            'name': 'High Traffic Volumetric Attack',
            'attack_type': 'ddos',
            'symbolic_conditions': ['high_traffic_rate', 'high_connections'],
            'conclusion': 'ddos_attack',
            'cf': 0.83,
            'priority': 'high',
            'severity_score': 8
        },
        {
            'name': 'Very High Traffic Severe DDoS',
            'attack_type': 'ddos',
            'symbolic_conditions': ['very_high_traffic_rate', 'very_high_connections'],
            'conclusion': 'ddos_attack',
            'cf': 0.95,
            'priority': 'high',
            'severity_score': 10
        },
        {
            'name': 'Bandwidth Exhaustion Attack',
            'attack_type': 'ddos',
            'symbolic_conditions': ['high_bandwidth', 'high_traffic_rate'],
            'conclusion': 'ddos_attack',
            'cf': 0.88,
            'priority': 'high',
            'severity_score': 9
        },
        {
            'name': 'External Flood Attack',
            'attack_type': 'ddos',
            'symbolic_conditions': ['external_source', 'high_traffic_rate', 'high_connections'],
            'conclusion': 'ddos_attack',
            'cf': 0.90,
            'priority': 'high',
            'severity_score': 9
        },
        {
            'name': 'Extreme Traffic Attack',
            'attack_type': 'ddos',
            'symbolic_conditions': ['extreme_traffic_rate'],
            'conclusion': 'ddos_attack',
            'cf': 0.93,
            'priority': 'high',
            'severity_score': 10
        },
        {
            'name': 'Sustained High Value Target Attack',
            'attack_type': 'unauthorized_access',
            'symbolic_conditions': ['sustained_attack', 'high_value_target'],
            'conclusion': 'apt_attack',
            'cf': 0.78,
            'priority': 'high',
            'severity_score': 9
        }
    ]
    
    created_count = 0
    skipped_count = 0
    updated_count = 0
    
    for data in rules_data:
        attack_type_name = data.pop('attack_type')
        attack_type = AttackType.query.filter_by(name=attack_type_name).first()
        
        if not attack_type:
            print(f"  ⚠ Attack type '{attack_type_name}' not found, skipping rule '{data['name']}'")
            skipped_count += 1
            continue
        
        existing = Rule.query.filter_by(name=data['name']).first()
        if existing:
            existing.symbolic_conditions = data['symbolic_conditions']
            existing.conclusion = data['conclusion']
            existing.cf = data['cf']
            existing.priority = data.get('priority', existing.priority)
            existing.severity_score = data.get('severity_score', existing.severity_score)
            existing.is_active = True
            updated_count += 1
            print(f"  ✓ Updated rule: {data['name']} (CF={data['cf']})")
        else:
            rule = Rule(
                attack_type_id=attack_type.id,
                is_active=True,
                **data
            )
            db.session.add(rule)
            created_count += 1
            print(f"  ✓ Created rule: {data['name']} (CF={data['cf']})")
    
    db.session.commit()
    return created_count, updated_count, skipped_count


def main():
    app = create_app()
    
    with app.app_context():
        print("\n" + "=" * 70)
        print("Seeding Forward-Chaining Rules with Certainty Factors")
        print("=" * 70 + "\n")
        
        try:
            created, updated, skipped = seed_rules_new_engine()
            
            print("\n" + "=" * 70)
            print("✓ Rule seeding completed!")
            print("=" * 70)
            print(f"\nResults:")
            print(f"  - Created: {created}")
            print(f"  - Updated: {updated}")
            print(f"  - Skipped: {skipped}")
            print("=" * 70 + "\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    main()
