from fastapi import APIRouter, Body, Depends
from typing import Annotated
from random import randrange

router = APIRouter()

@router.get("/api1/{id}")
async def api1_copay_data(id: str):
    valid_response = {
        "status_code": 200,
        "id": id,
        "oop_max": 10000,
        "remaining_oop_max": 9000,
        "copay": 1000
    }
    invalid_response = {
        "status_code": 500,
        "message": "internal server error"
    }
    return valid_response if randrange(100) > 10 else invalid_response

@router.get("/api2/{id}")
async def api2_copay_data(id: str):
    valid_response = {
        "status_code": 200,
        "id": id,
        "oop_max": 20000,
        "remaining_oop_max": 9000,
        "copay": 50000 
    }
    invalid_response = {
        "status_code": 500,
        "message": "internal server error"
    }
    return valid_response if randrange(100) > 10 else invalid_response

@router.get("/api3/{id}")
async def api3_copay_data(id: str):
    valid_response = {
        "status_code": 200,
        "id": id,
        "oop_max": 10000,
        "remaining_oop_max": 9000,
        "copay": 1000
    }
    invalid_response = {
        "status_code": 500,
        "message": "internal server error"
    }
    return valid_response if randrange(100) > 10 else invalid_response
