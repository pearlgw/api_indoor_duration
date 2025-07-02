#!/usr/bin/env python3
"""
Script untuk generate migration otomatis berdasarkan perubahan model
"""
import os
import sys
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_migration(message=None):
    """Generate migration otomatis"""
    if not message:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        message = f"auto_migration_{timestamp}"
    
    print(f"🚀 Generating migration: {message}")
    
    try:
        # Generate migration dengan alembic
        cmd = ["alembic", "revision", "--autogenerate", "-m", message]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Migration generated successfully!")
            print(result.stdout)
        else:
            print("❌ Error generating migration:")
            print(result.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

def run_migration():
    """Run migration yang sudah di-generate"""
    print("🚀 Running migrations...")
    
    try:
        cmd = ["alembic", "upgrade", "head"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Migrations applied successfully!")
            print(result.stdout)
        else:
            print("❌ Error running migrations:")
            print(result.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate and run migrations")
    parser.add_argument("--message", "-m", help="Migration message")
    parser.add_argument("--run", "-r", action="store_true", help="Run migrations after generating")
    
    args = parser.parse_args()
    
    generate_migration(args.message)
    
    if args.run:
        run_migration() 