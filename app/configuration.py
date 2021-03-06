import os


VERSION = os.getenv("VERSION", "0.1.0")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
SECRET_KEY = os.getenv("SECRET_KEY", "")
SECRET_KEY_MIDDLEWARE = os.getenv("SECRET_KEY_MIDDLEWARE", "")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

MONGO_DB = os.environ.get("MONGO_DB", "db")
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://user:password@localhost/db")