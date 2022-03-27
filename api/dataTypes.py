from pydantic import BaseModel
from datetime import datetime


class User_cred(BaseModel):
    loginId: str
    password: str


class Auth_details(BaseModel):
    loginId: str
    uuidId: str
    jwt_token: str


class Transaction_details(BaseModel):
    sender: str
    receiver: str
    amount: float
    curr: str
    title: str
    time: datetime
    auth_details: Auth_details
