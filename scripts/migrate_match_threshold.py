"""
Migration script to add match_threshold column to existing rules
Run this once to update existing database records
"""
import sys
import os
import sqlite3

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db
from config import Config

def migrate_match_threshold():
    """Add match_threshold column to existing rules"""
    app = create_app()
    
    with app.app_context():
        # Get database path
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        db_path = db_uri.replace('sqlite:///', '')
        
        print(f"📂 Database: {db_path}")
        
        # Connect directly with sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            # Check if column exists
            cursor.execute("PRAGMA table_info(rules)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'match_threshold' in columns:
                print("✅ match_threshold column already exists!")
                
                # Update any NULL values to default
                cursor.execute("UPDATE rules SET match_threshold = 0.7 WHERE match_threshold IS NULL OR match_threshold = 0")
                updated = cursor.rowcount
                conn.commit()
                
                if updated > 0:
                    print(f"✅ Updated {updated} rule(s) with default threshold (70%)")
                else:
                    print("✅ All rules already have valid match_threshold!")
                
            else:
                print("⚠️  Adding match_threshold column...")
                
                # Add the column with default value
                cursor.execute("ALTER TABLE rules ADD COLUMN match_threshold REAL DEFAULT 0.7 NOT NULL")
                conn.commit()
                
                print("✅ Column added successfully!")
                
                # Verify and show count
                cursor.execute("SELECT COUNT(*) FROM rules")
                rule_count = cursor.fetchone()[0]
                print(f"✅ {rule_count} rule(s) migrated with default 70% threshold")
                
        except sqlite3.Error as e:
            print(f"❌ Database error: {e}")
            conn.rollback()
        finally:
            conn.close()

if __name__ == '__main__':
    print("🔧 Match Threshold Migration Script")
    print("=" * 50)
    migrate_match_threshold()
    print("\n✨ Migration complete! You can now run the app.")
