"""
Authentication API Routes - Database Connected
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets

from app.models.auth import Token, TokenRefreshRequest, PasswordResetRequest, PasswordResetConfirm
from app.models.common import APIResponse
from app.core.security import (
    create_access_token, create_refresh_token, verify_password, 
    get_password_hash, get_current_user
)
from app.core.config import settings
from app.db.database import get_db
from app.db.models import User, Session as UserSession, PasswordResetToken, LoginAuditLog

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticate user and return tokens"""
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Log attempt
    log = LoginAuditLog(
        email=form_data.username,
        action="login_failed" if not user else "login_attempt",
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent", "")[:500]
    )
    
    if not user:
        db.add(log)
        db.commit()
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(form_data.password, user.password_hash):
        log.user_id = user.id
        db.add(log)
        db.commit()
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id, "role": user.role.value}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email, "user_id": user.id}
    )
    
    # Store session
    session = UserSession(
        user_id=user.id,
        refresh_token=refresh_token,
        device_info=request.headers.get("user-agent", "")[:255],
        ip_address=request.client.host if request.client else None,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.add(session)
    
    # Update last login
    user.last_login = datetime.utcnow()
    
    # Success log
    log.action = "login_success"
    log.user_id = user.id
    db.add(log)
    db.commit()
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/logout")
async def logout(
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Logout user and invalidate session"""
    # Get auth header
    auth_header = request.headers.get("authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
        # Delete all sessions for this user (simple approach)
        db.query(UserSession).filter(UserSession.user_id == current_user["user_id"]).delete()
        db.commit()
    
    # Log logout
    log = LoginAuditLog(
        user_id=current_user["user_id"],
        email=current_user.get("email", ""),
        action="logout",
        ip_address=request.client.host if request.client else None
    )
    db.add(log)
    db.commit()
    
    return APIResponse(message="Logged out successfully")


@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: TokenRefreshRequest,
    db: Session = Depends(get_db)
):
    """Refresh access token"""
    session = db.query(UserSession).filter(
        UserSession.refresh_token == request.refresh_token,
        UserSession.expires_at > datetime.utcnow()
    ).first()
    
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    user = db.query(User).filter(User.id == session.user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    
    # Create new access token
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id, "role": user.role.value}
    )
    
    # Optionally rotate refresh token
    new_refresh_token = create_refresh_token(
        data={"sub": user.email, "user_id": user.id}
    )
    session.refresh_token = new_refresh_token
    session.expires_at = datetime.utcnow() + timedelta(days=7)
    db.commit()
    
    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/password-reset/request")
async def request_password_reset(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """Request password reset email"""
    user = db.query(User).filter(User.email == request.email).first()
    
    # Always return success to prevent email enumeration
    if not user:
        return APIResponse(message="If the email exists, a reset link has been sent")
    
    # Generate token
    token = secrets.token_urlsafe(32)
    reset = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(hours=1)
    )
    db.add(reset)
    db.commit()
    
    # In production, send email here
    # For now, just return success
    return APIResponse(
        message="If the email exists, a reset link has been sent",
        data={"token": token}  # Remove this in production!
    )


@router.post("/password-reset/confirm")
async def confirm_password_reset(
    request: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """Confirm password reset with token"""
    reset = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == request.token,
        PasswordResetToken.expires_at > datetime.utcnow(),
        PasswordResetToken.used == False
    ).first()
    
    if not reset:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    user = db.query(User).filter(User.id == reset.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update password
    user.password_hash = get_password_hash(request.new_password)
    reset.used = True
    
    # Invalidate all sessions
    db.query(UserSession).filter(UserSession.user_id == user.id).delete()
    
    db.commit()
    
    return APIResponse(message="Password reset successfully")


@router.get("/me")
async def get_current_user_info(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get current user information"""
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "phone": user.phone,
        "role": user.role.value,
        "is_active": user.is_active,
        "last_login": user.last_login,
        "created_at": user.created_at
    }
