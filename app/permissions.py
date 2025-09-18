from fastapi import Depends, HTTPException, status
from typing import List


# Example: In a real app, get current user from auth token/session
class User:
    def __init__(self, role: str):
        self.role = role


def get_current_user(role: str = "teacher"):
    # In production, extract user/role from JWT or session
    return User(role=role)


def require_roles(allowed_roles: List[str]):
    def dependency(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted for role: {current_user.role}"
            )
        return current_user
    return dependency
