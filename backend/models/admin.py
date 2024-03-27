from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr

class Admin(Document):
    fullname: str
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Ragnaros",
                "email": "molten@core.com",
                "password": "sulfuras",
            }
        }

    class Settings:
        name = "admin"

class AdminSignIn(HTTPBasicCredentials):
    class Config:
        json_schema_extra = {
            "example": {"username": "Nefarian", "password": "theblackwinglair"}
        }

class AdminData(BaseModel):
    fullname: str
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Onyxia",
                "email": "onixya@lair.com",
            }
        }
