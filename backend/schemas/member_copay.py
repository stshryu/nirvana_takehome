from pydantic import BaseModel
from typing import Optional, Any

class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Config:
        json_schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Successfully got member copay data",
                "data": { 
                    "oop_max": 10000,
                    "remaining_oop_max": 9000,
                    "copay": 1000,
                },
            }
        }
