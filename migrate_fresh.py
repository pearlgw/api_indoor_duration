#!/usr/bin/env python3
"""
Script untuk melakukan migrate:fresh (drop semua tabel dan recreate)
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database, drop_database
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.config.config import DATABASE_URL, Base, engine
from app.models.api_key import ApiKey
from app.models.person_duration import PersonDuration
from app.models.detail_person_duration import DetailPersonDuration

def migrate_fresh():
    """Drop semua tabel dan recreate dari awal"""
    print("🚀 Starting migrate:fresh...")
    
    try:
        # Drop semua tabel yang ada
        print("🗑️  Dropping all existing tables...")
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped successfully")
        
        # Create semua tabel baru
        print("🏗️  Creating all tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully")
        
        print("🎉 Migrate:fresh completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during migrate:fresh: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    migrate_fresh() 