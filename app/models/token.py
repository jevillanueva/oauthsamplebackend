from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    expires: timedelta
    date_expires: datetime


class TokenData(BaseModel):
    id: Optional[str]= None
    username: Optional[str] = None
