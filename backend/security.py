from fastapi import Header, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def check_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        print("API_KEY =", API_KEY)
        raise HTTPException(status_code=403, detail="Forbidden")
