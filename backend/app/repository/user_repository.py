from sqlalchemy.orm import Session
from sqlalchemy import or_
from uuid import UUID

from app.models.user_models import User
from app.schemas.user_schema import UserCreate


def get_user_by_email(db: Session, email: str):

    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):

    return db.query(User).filter(User.id == user_id).first()


def get_user_by_uuid(db: Session, user_uuid: UUID):

    return db.query(User).filter(User.uuid == user_uuid).first()


def check_user_exists(db: Session, email: str, contact: str):

    return db.query(User).filter(
        or_(User.email == email, User.contact == contact)
    ).first()


def create_user(db: Session, user: UserCreate, password_hash: str):

    existing_user = check_user_exists(db, user.email, user.contact)

    if existing_user:
        raise ValueError("User with same email or contact already exists")

    new_user = User(
        name=user.name,
        email=user.email,
        contact=user.contact,
        profile_pic=user.profile_pic,
        address=user.address,
        role=user.role,
        password_hash=password_hash
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def update_user(db: Session, user: User, update_data: dict):

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user: User):

    db.delete(user)
    db.commit()

    return True