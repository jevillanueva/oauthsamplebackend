from bson import ObjectId
from pydantic import Field
from app.validators.mongo import PyObjectId
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    expires: timedelta
    date_expires: datetime


class TokenData(BaseModel):
    jti: str
    username: Optional[str] = None

class TokenDataInDB(TokenData):
    id: Optional[PyObjectId] = Field(alias="_id")
    revoked: bool = False
    expire_at: Optional[datetime] = None
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }