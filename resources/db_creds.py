import os

from dotenv import load_dotenv

load_dotenv()


class DBCreds:
    DBNAME = os.getenv("DBNAME")
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")
    USER_BD = os.getenv("USER_BD")
    PASSWORD = os.getenv("PASSWORD")
