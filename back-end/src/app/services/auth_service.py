from sqlalchemy.orm import Session
from repository.user_repo import get_user_by_email, create_user
from utils.auth_utils import hash_password, verify_password, create_access_token

def register_user(db: Session, email: str, password: str):
    existing_user = get_user_by_email(db, email)
    if existing_user:
        raise Exception("User already exists")

    hashed_password = hash_password(password)
    user = create_user(db, email, hashed_password)
    return user

def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        raise Exception("Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise Exception("Invalid credentials")

    token = create_access_token({"sub": user.email})
    return token