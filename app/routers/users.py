from app.models.user import User
from app.token import get_current_active_user
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user