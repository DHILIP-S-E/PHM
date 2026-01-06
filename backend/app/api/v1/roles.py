"""
Roles Management API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import json

from app.db.database import get_db
from app.db.models import Role, User, UserRole
from app.models.auth import RoleCreate, RoleResponse
from pydantic import BaseModel

router = APIRouter()


class RoleListResponse(BaseModel):
    items: list[RoleResponse]
    total: int


class RoleUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[list[str]] = None


class AssignRoleRequest(BaseModel):
    user_id: str
    role_id: str


@router.get("", response_model=RoleListResponse)
async def list_roles(
    db: Session = Depends(get_db)
):
    """List all roles"""
    roles = db.query(Role).all()
    
    role_responses = []
    for role in roles:
        permissions = json.loads(role.permissions) if role.permissions else []
        role_responses.append(RoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            permissions=permissions,
            created_at=role.created_at
        ))
    
    return RoleListResponse(items=role_responses, total=len(roles))


@router.post("", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db)
):
    """Create a new role"""
    # Check if role name already exists
    existing = db.query(Role).filter(Role.name == role_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role with name '{role_data.name}' already exists"
        )
    
    role = Role(
        name=role_data.name,
        description=role_data.description,
        permissions=json.dumps(role_data.permissions),
        is_system=False
    )
    
    db.add(role)
    db.commit()
    db.refresh(role)
    
    return RoleResponse(
        id=role.id,
        name=role.name,
        description=role.description,
        permissions=role_data.permissions,
        created_at=role.created_at
    )


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: str,
    db: Session = Depends(get_db)
):
    """Get a role by ID"""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    permissions = json.loads(role.permissions) if role.permissions else []
    return RoleResponse(
        id=role.id,
        name=role.name,
        description=role.description,
        permissions=permissions,
        created_at=role.created_at
    )


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: str,
    update_data: RoleUpdateRequest,
    db: Session = Depends(get_db)
):
    """Update a role"""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    if role.is_system:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify system roles"
        )
    
    if update_data.name is not None:
        role.name = update_data.name
    if update_data.description is not None:
        role.description = update_data.description
    if update_data.permissions is not None:
        role.permissions = json.dumps(update_data.permissions)
    
    db.commit()
    db.refresh(role)
    
    permissions = json.loads(role.permissions) if role.permissions else []
    return RoleResponse(
        id=role.id,
        name=role.name,
        description=role.description,
        permissions=permissions,
        created_at=role.created_at
    )


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: str,
    db: Session = Depends(get_db)
):
    """Delete a role"""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    if role.is_system:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete system roles"
        )
    
    # Check if role is assigned to any users
    user_roles = db.query(UserRole).filter(UserRole.role_id == role_id).count()
    if user_roles > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete role. It is assigned to {user_roles} user(s)"
        )
    
    db.delete(role)
    db.commit()


@router.post("/{role_id}/users/{user_id}", status_code=status.HTTP_201_CREATED)
async def assign_role_to_user(
    role_id: str,
    user_id: str,
    db: Session = Depends(get_db)
):
    """Assign a role to a user"""
    # Verify role exists
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if already assigned
    existing = db.query(UserRole).filter(
        UserRole.user_id == user_id,
        UserRole.role_id == role_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role already assigned to user"
        )
    
    user_role = UserRole(user_id=user_id, role_id=role_id)
    db.add(user_role)
    db.commit()
    
    return {"message": "Role assigned successfully"}


@router.delete("/{role_id}/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_role_from_user(
    role_id: str,
    user_id: str,
    db: Session = Depends(get_db)
):
    """Remove a role from a user"""
    user_role = db.query(UserRole).filter(
        UserRole.user_id == user_id,
        UserRole.role_id == role_id
    ).first()
    
    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role assignment not found"
        )
    
    db.delete(user_role)
    db.commit()
