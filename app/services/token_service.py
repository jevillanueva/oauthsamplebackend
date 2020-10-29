from pymongo.collection import ReturnDocument
from app.database import db
from app.models.token import TokenDataInDB


def insert_token(token: TokenDataInDB):
  if (hasattr(token, "id")):
    delattr(token, "id")
  if (hasattr(token, "username")):
    delattr(token, "username")
  ret = db.jwt.insert_one(token.dict(by_alias=True))
  token.id = ret.inserted_id
  return token

def token_revoke(token: TokenDataInDB):
  ret = db.jwt.find_one({"jti": token.jti})
  if ret is None:
    return True
  else:
    find = TokenDataInDB(**ret)
    return find.revoked == True

def revoke_token(token: TokenDataInDB):
  token.revoked = True
  ret = db.jwt.find_one_and_update({"jti": token.jti}, {"$set": {"revoked": token.revoked}}, return_document=ReturnDocument.AFTER, upsert=True )
  if ret is not None:
    return TokenDataInDB(**ret)
  else:
    return None