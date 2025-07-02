#!/usr/bin/env python3
"""
Database Management Script for API Indoor Duration
This script provides utilities for database operations including migrations.
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def check_docker():
    """Check if Docker is running"""
    return run_command("docker --version", "Checking Docker installation")

def start_database():
    """Start PostgreSQL database using Docker Compose"""
    print("\n🐳 Starting PostgreSQL database...")
    if not run_command("docker-compose up -d postgres", "Starting PostgreSQL container"):
        return False
    
    print("⏳ Waiting for database to be ready...")
    import time
    time.sleep(10)  # Wait for database to start
    return True

def stop_database():
    """Stop PostgreSQL database"""
    return run_command("docker-compose down", "Stopping PostgreSQL container")

def init_migrations():
    """Initialize Alembic migrations"""
    return run_command("alembic init alembic", "Initializing Alembic migrations")

def create_migration(message):
    """Create a new migration"""
    return run_command(f'alembic revision --autogenerate -m "{message}"', f"Creating migration: {message}")

def run_migrations():
    """Run all pending migrations"""
    return run_command("alembic upgrade head", "Running migrations")

def show_migration_status():
    """Show current migration status"""
    return run_command("alembic current", "Showing migration status")

def show_migration_history():
    """Show migration history"""
    return run_command("alembic history", "Showing migration history")

def reset_database():
    """Reset database (drop all tables and recreate)"""
    print("\n⚠️  WARNING: This will delete all data in the database!")
    confirm = input("Are you sure you want to continue? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Operation cancelled.")
        return False
    
    return run_command("alembic downgrade base", "Dropping all tables") and \
           run_command("alembic upgrade head", "Recreating all tables")

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 2:
        print("""
Database Management Script for API Indoor Duration

Usage:
    python db_manage.py <command>

Commands:
    start-db      - Start PostgreSQL database
    stop-db       - Stop PostgreSQL database
    init          - Initialize Alembic migrations
    migrate       - Run all pending migrations
    create-mig    - Create a new migration (requires message)
    status        - Show current migration status
    history       - Show migration history
    reset         - Reset database (drop all tables and recreate)
    setup         - Complete setup (start db, run migrations)

Examples:
    python db_manage.py start-db
    python db_manage.py create-mig "Add user table"
    python db_manage.py migrate
    python db_manage.py setup
        """)
        return

    command = sys.argv[1]

    if command == "start-db":
        start_database()
    elif command == "stop-db":
        stop_database()
    elif command == "init":
        init_migrations()
    elif command == "migrate":
        run_migrations()
    elif command == "create-mig":
        if len(sys.argv) < 3:
            print("❌ Error: Migration message is required")
            print("Usage: python db_manage.py create-mig \"Your migration message\"")
            return
        message = sys.argv[2]
        create_migration(message)
    elif command == "status":
        show_migration_status()
    elif command == "history":
        show_migration_history()
    elif command == "reset":
        reset_database()
    elif command == "setup":
        print("🚀 Setting up complete database environment...")
        if check_docker() and start_database() and run_migrations():
            print("\n🎉 Database setup completed successfully!")
            print("You can now run your FastAPI application.")
        else:
            print("\n❌ Database setup failed!")
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'python db_manage.py' for help.")

if __name__ == "__main__":
    main() 