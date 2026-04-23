#!/usr/bin/env python3
"""
Simple script to add a user to the SQLite database
"""
import sqlite3
import uuid
import hashlib
import os
from datetime import datetime
from pathlib import Path

# For bcrypt hashing
try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    USE_PASSLIB = True
except ImportError:
    USE_PASSLIB = False
    print("Warning: passlib not installed, using simple hash instead")

def hash_password(password: str):
    """Hash password using bcrypt or simple hash fallback"""
    if USE_PASSLIB:
        return pwd_context.hash(password)
    else:
        # Simple fallback hash (not secure, for testing only)
        return hashlib.sha256(password.encode()).hexdigest()

def add_user(db_path: str, email: str, password: str):
    """Add user to database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            print(f"✗ User with email '{email}' already exists!")
            conn.close()
            return False
        
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
        
        print(f"✓ User '{email}' created successfully!")
        print(f"  ID: {user_id}")
        print(f"  Password hash created at: {created_at}")
        return True
        
    except sqlite3.OperationalError as e:
        print(f"✗ Database error: {e}")
        print("  Make sure the database exists and has a 'users' table")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python3 add_user_sqlite.py <email> <password>")
        print("Example: python3 add_user_sqlite.py test@example.com mypassword")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    
    # Path to database (relative to back-end directory)
    db_path = "src/app/ai_interview.db"
    
    if not os.path.exists(db_path):
        print(f"✗ Database file not found: {db_path}")
        sys.exit(1)
    
    success = add_user(db_path, email, password)
    sys.exit(0 if success else 1)
