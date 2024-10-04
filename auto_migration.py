import os
from flask_migrate import Migrate, upgrade, migrate
from app import app, db  

def run_migrations():
    """Automatically detect, create migration, and apply migration."""
    with app.app_context():
        # Create new migration script by detecting changes
        print("Detecting changes and creating migration script...")
        migrate(message="Auto-detected migration")
        
        # Apply the migration to the database
        print("Applying migration to the database...")
        upgrade()

        print("Migrations successfully applied.")

if __name__ == '__main__':
    run_migrations()
