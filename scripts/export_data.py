#!/usr/bin/env python3
"""
Export database data to JSON files for migration
Usage: python scripts/export_data.py
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.models.attack_type import AttackType
from app.models.rule import Rule
from extensions import db


def export_data():
    """Export attack types and rules to JSON"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "=" * 70)
        print("Exporting Database Data")
        print("=" * 70 + "\n")
        
        # Create exports directory
        export_dir = 'database_exports'
        os.makedirs(export_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Export Attack Types
        print("Exporting Attack Types...")
        attack_types = AttackType.query.all()
        attack_types_data = []
        
        for at in attack_types:
            attack_types_data.append({
                'name': at.name,
                'description': at.description,
                'severity_level': at.severity_level,
                'is_active': at.is_active
            })
        
        attack_types_file = os.path.join(export_dir, f'attack_types_{timestamp}.json')
        with open(attack_types_file, 'w') as f:
            json.dump(attack_types_data, f, indent=2)
        print(f"  ✓ Exported {len(attack_types_data)} attack types to: {attack_types_file}")
        
        # Export Rules
        print("\nExporting Security Rules...")
        rules = Rule.query.all()
        rules_data = []
        
        for rule in rules:
            rules_data.append({
                'name': rule.name,
                'attack_type_name': rule.attack_type.name,
                'symbolic_conditions': rule.symbolic_conditions,
                'conclusion': rule.conclusion,
                'cf': rule.cf,
                'is_active': rule.is_active
            })
        
        rules_file = os.path.join(export_dir, f'rules_{timestamp}.json')
        with open(rules_file, 'w') as f:
            json.dump(rules_data, f, indent=2)
        print(f"  ✓ Exported {len(rules_data)} rules to: {rules_file}")
        
        print("\n" + "=" * 70)
        print("✓ Export completed successfully!")
        print("=" * 70)
        print(f"\nExported files:")
        print(f"  - {attack_types_file}")
        print(f"  - {rules_file}")
        print(f"\nTo import on server, upload these files and run:")
        print(f"  python import_data.py {os.path.basename(attack_types_file)} {os.path.basename(rules_file)}")
        print("=" * 70 + "\n")


if __name__ == "__main__":
    export_data()
