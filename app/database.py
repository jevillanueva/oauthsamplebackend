db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",#Secret
        "disabled": False,
    }
}
revoked = []
# def UpsertUser()
def set_revoke_token(id: str):
  revoked.append(id)

def is_revoked(id:str):
  return id in revoked
