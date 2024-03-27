from fastapi import APIRouter, Body
from schemas.member_copay import Response
from services import copay_retrieval_service as CopayService
import success
import errors

router = APIRouter()

@router.get("/{id}", response_description="Member Copay data retrieved", response_model=Response)
async def get_member_copay_data(id: str):
    # The line below demonstrates how we might decouple retrieving the copay data.
    # await enqueue_copay_jobs(id)

    # For testing's sake we're using a simpler version of the job scheduling below, by mocking out the data we'll receive.
    response = await CopayService.get_copay_data(id)
    match response:
        case success.Success():
            return {
                "status_code": 200,
                "response_type": "success",
                "description": "Successfully got member copay data and smoothed it for id: {}".format(id),
                "data": response.unpack()
            }
        case errors.NotEnoughDataError():
            return {
                "status_code": 500,
                "response_type": "error",
                "description": "Not enough data received",
                "data": response.toJson() 
            }
        case _:
            return {
                "status_code": 500,
                "response_type": "UnexpectedError",
                "description": "Error retrieving data",
                "data": None
            }
