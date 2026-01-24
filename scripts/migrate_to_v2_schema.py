"""
Migrate database schema from v1 to v2
Removes old v1 fields from incidents and rules tables
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from extensions import db


def migrate_schema():
    """Migrate database schema to v2"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "=" * 70)
        print("Migrating Database Schema to V2")
        print("=" * 70 + "\n")
        
        try:
            # Get database connection
            with db.engine.connect() as conn:
                
                # Check if incidents table exists
                print("Checking incidents table...")
                result = conn.execute(db.text("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents'"))
                if not result.fetchone():
                    print("  ⚠ Incidents table not found, skipping...")
                else:
                    # Check for old columns in incidents
                    result = conn.execute(db.text("PRAGMA table_info(incidents)"))
                    columns = {row[1] for row in result.fetchall()}
                    
                    if 'confidence_score' in columns or 'matched_rules' in columns:
                        print("  Found old v1 columns in incidents table")
                        print("  Creating new incidents table without v1 columns...")
                        
                        # Create new table structure
                        conn.execute(db.text("""
                            CREATE TABLE incidents_new (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                alert_id INTEGER NOT NULL,
                                attack_type_id INTEGER,
                                conclusions JSON,
                                trace JSON,
                                final_cf FLOAT,
                                recommended_actions JSON,
                                explanation TEXT,
                                status VARCHAR(20) NOT NULL DEFAULT 'new',
                                assigned_to INTEGER,
                                created_at DATETIME NOT NULL,
                                updated_at DATETIME NOT NULL,
                                resolved_at DATETIME,
                                FOREIGN KEY (alert_id) REFERENCES alerts(id),
                                FOREIGN KEY (attack_type_id) REFERENCES attack_types(id),
                                FOREIGN KEY (assigned_to) REFERENCES users(id),
                                UNIQUE (alert_id)
                            )
                        """))
                        conn.commit()
                        
                        # Copy data from old to new table
                        print("  Copying data to new table...")
                        conn.execute(db.text("""
                            INSERT INTO incidents_new 
                            (id, alert_id, attack_type_id, conclusions, trace, final_cf, 
                             recommended_actions, explanation, status, assigned_to, 
                             created_at, updated_at, resolved_at)
                            SELECT 
                                id, alert_id, attack_type_id, conclusions, trace, final_cf,
                                recommended_actions, explanation, status, assigned_to,
                                created_at, updated_at, resolved_at
                            FROM incidents
                        """))
                        conn.commit()
                        
                        # Drop old table and rename new one
                        print("  Replacing old table with new one...")
                        conn.execute(db.text("DROP TABLE incidents"))
                        conn.commit()
                        conn.execute(db.text("ALTER TABLE incidents_new RENAME TO incidents"))
                        conn.commit()
                        
                        print("  ✓ Incidents table migrated successfully")
                    else:
                        print("  ✓ Incidents table already v2 compliant")
                
                # Check if rules table exists
                print("\nChecking rules table...")
                result = conn.execute(db.text("SELECT name FROM sqlite_master WHERE type='table' AND name='rules'"))
                if not result.fetchone():
                    print("  ⚠ Rules table not found, skipping...")
                else:
                    # Check for old columns in rules
                    result = conn.execute(db.text("PRAGMA table_info(rules)"))
                    columns = {row[1] for row in result.fetchall()}
                    
                    if 'conditions' in columns or 'actions' in columns or 'priority' in columns or 'severity_score' in columns or 'match_threshold' in columns:
                        print("  Found old v1 columns in rules table")
                        print("  Creating new rules table without v1 columns...")
                        
                        # Create new table structure
                        conn.execute(db.text("""
                            CREATE TABLE rules_new (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name VARCHAR(200) NOT NULL,
                                attack_type_id INTEGER NOT NULL,
                                symbolic_conditions JSON,
                                conclusion VARCHAR(100),
                                cf FLOAT,
                                is_active BOOLEAN NOT NULL DEFAULT 1,
                                created_at DATETIME NOT NULL,
                                updated_at DATETIME NOT NULL,
                                FOREIGN KEY (attack_type_id) REFERENCES attack_types(id)
                            )
                        """))
                        conn.commit()
                        
                        # Copy data from old to new table
                        print("  Copying data to new table...")
                        conn.execute(db.text("""
                            INSERT INTO rules_new 
                            (id, name, attack_type_id, symbolic_conditions, conclusion, cf,
                             is_active, created_at, updated_at)
                            SELECT 
                                id, name, attack_type_id, symbolic_conditions, conclusion, cf,
                                is_active, created_at, updated_at
                            FROM rules
                        """))
                        conn.commit()
                        
                        # Drop old table and rename new one
                        print("  Replacing old table with new one...")
                        conn.execute(db.text("DROP TABLE rules"))
                        conn.commit()
                        conn.execute(db.text("ALTER TABLE rules_new RENAME TO rules"))
                        conn.commit()
                        
                        print("  ✓ Rules table migrated successfully")
                    else:
                        print("  ✓ Rules table already v2 compliant")
                
                print("\n" + "=" * 70)
                print("✓ Schema migration completed successfully!")
                print("=" * 70 + "\n")
                
        except Exception as e:
            print(f"\n✗ Migration failed: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    migrate_schema()
