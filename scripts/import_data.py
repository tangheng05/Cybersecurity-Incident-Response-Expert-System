#!/usr/bin/env python3
"""
Import database data from JSON files
Usage: python scripts/import_data.py [attack_types_file.json] [rules_file.json]
"""
import json
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.models.attack_type import AttackType
from app.models.rule import Rule
from extensions import db


def import_attack_types(file_path):
    """Import attack types from JSON file"""
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return 0, 0
    
    with open(file_path, 'r') as f:
        attack_types_data = json.load(f)
    
    created_count = 0
    skipped_count = 0
    
    print(f"Importing Attack Types from: {file_path}")
    
    for data in attack_types_data:
        existing = AttackType.query.filter_by(name=data['name']).first()
        if existing:
            print(f"  ⊘ Attack type '{data['name']}' already exists, skipping...")
            skipped_count += 1
            continue
        
        attack_type = AttackType(**data)
        db.session.add(attack_type)
        created_count += 1
        print(f"  ✓ Imported attack type: {data['name']}")
    
    db.session.commit()
    return created_count, skipped_count


def import_rules(file_path):
    """Import rules from JSON file"""
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return 0, 0
    
    with open(file_path, 'r') as f:
        rules_data = json.load(f)
    
    created_count = 0
    skipped_count = 0
    
    print(f"\nImporting Security Rules from: {file_path}")
    
    for data in rules_data:
        # Find the attack type
        attack_type_name = data.pop('attack_type_name')
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
        print(f"  ✓ Imported rule: {data['name']}")
    
    db.session.commit()
    return created_count, skipped_count


def main():
    """Main import function"""
    if len(sys.argv) < 3:
        print("\nUsage: python import_data.py <attack_types_file.json> <rules_file.json>")
        print("\nExample:")
        print("  python import_data.py database_exports/attack_types_20260110_120000.json database_exports/rules_20260110_120000.json")
        sys.exit(1)
    
    attack_types_file = sys.argv[1]
    rules_file = sys.argv[2]
    
    app = create_app()
    
    with app.app_context():
        print("\n" + "=" * 70)
        print("Importing Database Data")
        print("=" * 70 + "\n")
        
        try:
            # Import attack types
            attack_created, attack_skipped = import_attack_types(attack_types_file)
            
            # Import rules
            rule_created, rule_skipped = import_rules(rules_file)
            
            print("\n" + "=" * 70)
            print("✓ Data import completed successfully!")
            print("=" * 70)
            print(f"\nTotal Results:")
            print(f"  - Attack Types: {attack_created} imported, {attack_skipped} skipped")
            print(f"  - Security Rules: {rule_created} imported, {rule_skipped} skipped")
            print("=" * 70 + "\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ Error during import: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    main()
