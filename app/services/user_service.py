from datetime import datetime

from pymongo.collection import ReturnDocument
from app.database import db
from app.models.user import UserInDB
def insert_or_update_user(user: UserInDB):
  if (hasattr(user, "id")):
    delattr(user, "id")
  finded = db.user.find_one({"username": user.username, "disabled": False})
  if finded is None:
    user.date_insert = datetime.utcnow()
    ret = db.user.insert_one(user.dict(by_alias=True))
  else:
    user.date_update = datetime.utcnow()
    ret = db.user.find_one_and_update({"username": user.username, "disabled": False}, {"$set": user.dict(by_alias=True)}, return_document=ReturnDocument.AFTER )
  print (ret)
  return ret

def get_user(user: UserInDB):
  ret = db.user.find_one({"username": user.username})
  if ret is not None:
    return UserInDB(**ret)
  else:
    return None