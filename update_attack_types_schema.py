"""
Migration script to add created_at and updated_at columns to attack_types table
"""
from app import create_app
from extensions import db
from datetime import datetime

app = create_app()

with app.app_context():
    # Add columns using raw SQL
    try:
        with db.engine.connect() as conn:
            # Check if columns exist first
            result = conn.execute(db.text("PRAGMA table_info(attack_types)"))
            columns = [row[1] for row in result]
            
            if 'created_at' not in columns:
                print("Adding created_at column...")
                conn.execute(db.text(
                    "ALTER TABLE attack_types ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL"
                ))
                conn.commit()
                print("✅ created_at column added")
            else:
                print("created_at column already exists")
            
            if 'updated_at' not in columns:
                print("Adding updated_at column...")
                conn.execute(db.text(
                    "ALTER TABLE attack_types ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL"
                ))
                conn.commit()
                print("✅ updated_at column added")
            else:
                print("updated_at column already exists")
        
        print("\n✅ Migration completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        raise
