"""
Database migration script for new inference engine schema
Run this to update existing database with new fields
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from extensions import db
from sqlalchemy import text

app = create_app()

def migrate():
    with app.app_context():
        print("Starting database migration...")
        
        try:
            with db.engine.connect() as conn:
                print("\n1. Adding new fields to rules table...")
                
                try:
                    conn.execute(text("ALTER TABLE rules ADD COLUMN symbolic_conditions JSON"))
                    print("   ✓ Added symbolic_conditions")
                except Exception as e:
                    print(f"   - symbolic_conditions already exists or error: {e}")
                
                try:
                    conn.execute(text("ALTER TABLE rules ADD COLUMN conclusion VARCHAR(100)"))
                    print("   ✓ Added conclusion")
                except Exception as e:
                    print(f"   - conclusion already exists or error: {e}")
                
                try:
                    conn.execute(text("ALTER TABLE rules ADD COLUMN cf FLOAT"))
                    print("   ✓ Added cf")
                except Exception as e:
                    print(f"   - cf already exists or error: {e}")
                
                print("\n2. Adding new fields to incidents table...")
                
                try:
                    conn.execute(text("ALTER TABLE incidents ADD COLUMN conclusions JSON"))
                    print("   ✓ Added conclusions")
                except Exception as e:
                    print(f"   - conclusions already exists or error: {e}")
                
                try:
                    conn.execute(text("ALTER TABLE incidents ADD COLUMN trace JSON"))
                    print("   ✓ Added trace")
                except Exception as e:
                    print(f"   - trace already exists or error: {e}")
                
                try:
                    conn.execute(text("ALTER TABLE incidents ADD COLUMN final_cf FLOAT"))
                    print("   ✓ Added final_cf")
                except Exception as e:
                    print(f"   - final_cf already exists or error: {e}")
                
                conn.commit()
            
            print("\n✅ Migration completed successfully!")
            print("\nNote: Old fields (conditions, actions, confidence_score) kept for backward compatibility")
            
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            return False
    
    return True

if __name__ == "__main__":
    success = migrate()
    sys.exit(0 if success else 1)
