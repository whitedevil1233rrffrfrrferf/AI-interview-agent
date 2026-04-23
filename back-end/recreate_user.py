#!/usr/bin/env python3
"""
Script to delete and recreate a user with proper bcrypt hashing
"""
import sqlite3
import uuid
import os
from datetime import datetime
from pathlib import Path

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """Hash password using bcrypt"""
    return pwd_context.hash(password)

def recreate_user(db_path: str, email: str, password: str):
    """Delete existing user and create a new one"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Delete existing user
        cursor.execute("DELETE FROM users WHERE email = ?", (email,))
        deleted = cursor.rowcount
        
        # Create user
        user_id = str(uuid.uuid4())
        hashed_password = hash_password(password)
        created_at = datetime.utcnow().isoformat()
        
        cursor.execute(
            """
            INSERT INTO users (id, email, password_hash, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, email, hashed_password, created_at)
        )
        
        conn.commit()
        conn.close()
        
        if deleted:
            print(f"✓ Deleted previous user with email '{email}'")
        print(f"✓ User '{email}' created successfully with bcrypt hashing!")
        print(f"  ID: {user_id}")
        print(f"  Created at: {created_at}")
        return True
        
    except sqlite3.OperationalError as e:
        print(f"✗ Database error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python recreate_user.py <email> <password>")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    
    db_path = "src/app/ai_interview.db"
    
    if not os.path.exists(db_path):
        print(f"✗ Database file not found: {db_path}")
        sys.exit(1)
    
    success = recreate_user(db_path, email, password)
    sys.exit(0 if success else 1)
