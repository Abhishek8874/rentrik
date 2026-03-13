"""
app/api/user_routes.py

PURPOSE OF THIS FILE:
Handles all CRUD (Create, Read, Update, Delete) for your users.

NOTE: Authentication is temporarily DISABLED for testing purposes.
      All endpoints are open — no token required.
      To re-enable auth, uncomment the lines marked # [AUTH].
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.db.session import get_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse, UserRole, Msg
from app.repository import user_repository
from app.core.security import get_password_hash
# [AUTH] from app.api.deps import get_current_user
from app.models.user_models import User

router = APIRouter(prefix="/users")


# ──────────────────────────────────────────────
# POST /users/   →  Create a new user (public)
# ──────────────────────────────────────────────
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_repository.check_user_exists(db, email=user.email, contact=user.contact)
    if db_user:
        raise HTTPException(status_code=400, detail="User with same email or contact already exists")

    password_hash = get_password_hash(user.password)
    new_user = user_repository.create_user(db=db, user=user, password_hash=password_hash)
    return new_user


# ──────────────────────────────────────────────
# GET /users/   →  Get all users
# ──────────────────────────────────────────────
@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    # [AUTH] current_user: User = Depends(get_current_user)
    # [AUTH] if current_user.role != UserRole.ADMIN:
    # [AUTH]     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required.")
    users = db.query(User).all()
    return users


# ──────────────────────────────────────────────
# GET /users/{user_id}   →  Get user by ID
# ──────────────────────────────────────────────
@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    # [AUTH] current_user: User = Depends(get_current_user)
    db_user = user_repository.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # [AUTH] if current_user.id != db_user.id and current_user.role != UserRole.ADMIN:
    # [AUTH]     raise HTTPException(status_code=403, detail="Not authorized to access this user")
    return db_user


# ──────────────────────────────────────────────
# GET /users/uuid/{user_uuid}   →  Get user by UUID
# ──────────────────────────────────────────────
@router.get("/uuid/{user_uuid}", response_model=UserResponse)
def get_user_by_uuid(user_uuid: UUID, db: Session = Depends(get_db)):
    db_user = user_repository.get_user_by_uuid(db, user_uuid=user_uuid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# ──────────────────────────────────────────────
# PUT /users/{user_id}   →  Update user
# ──────────────────────────────────────────────
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, update_data: UserUpdate, db: Session = Depends(get_db)):
    # [AUTH] current_user: User = Depends(get_current_user)
    db_user = user_repository.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # [AUTH] if current_user.id != db_user.id and current_user.role != UserRole.ADMIN:
    # [AUTH]     raise HTTPException(status_code=403, detail="Not authorized to update this user")
    updated_user = user_repository.update_user(db=db, user=db_user, update_data=update_data.model_dump(exclude_unset=True))
    return updated_user


# ──────────────────────────────────────────────
# DELETE /users/{user_id}   →  Delete user
# ──────────────────────────────────────────────
@router.delete("/{user_id}", response_model=Msg)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # [AUTH] current_user: User = Depends(get_current_user)
    db_user = user_repository.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # [AUTH] if current_user.id != db_user.id and current_user.role != UserRole.ADMIN:
    # [AUTH]     raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    user_repository.delete_user(db=db, user=db_user)
    return {"message": "users deleted successfully"}