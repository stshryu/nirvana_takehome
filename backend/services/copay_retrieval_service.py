from fastapi import Depends
from typing import Annotated
from config.config import get_redis_connection
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from statistics import mode
import success
import errors

from api_integrations.api_mock import * 

async def enqueue_copay_jobs(id: str):
    """
    If we were to enqueue the copay jobs and instead subscribe to a notification service when the API's have successfully been retrieved we can ensure that temporary outages and downtime can be nullified

    This method should push to a redis queue. 
    """
    pass

async def notifier_queue():
    """
    This method should subscribe to whatever notification service our workers that grab the API's is notifying towards.

    This method reads a completed job from the redis queue.
    """
    pass

async def get_copay_data(id: str):
    response = await task(id)
    return await analyze_copay_data(response)

async def analyze_copay_data(response: Annotated[list, "list of type httpx.Reponse"]):
    for i in response:
        print(i.json())
    data = [ CopayResponse(**i.json()) for i in response if i.json()["status_code"] == 200]
    total_sent = len(response)
    total_received = len(data)
    if await percent_recieved(total_sent, total_received):
        return success.Success(await smooth_data(data))
    else:
        return errors.NotEnoughDataError(total_sent, total_received) 

async def percent_recieved(
    total_sent: Annotated[int, "Total requests sent"], total_received: Annotated[int, "Total requests received"]):
    return True if total_received / total_sent > .8 else False

async def smooth_data(returned_results):
    mode_copay = mode([i.copay for i in returned_results])
    mode_oop_max = mode([i.oop_max for i in returned_results])
    mode_remaining = mode([i.remaining_oop_max for i in returned_results])
    return {
        "status": "success",
        "oop_max": mode_oop_max,
        "remaining_oop_max": mode_remaining,
        "copay": mode_copay
    }

@dataclass
class CopayResponse:
    """
    Mock dataclass for the CopayResponse (we'd probably want to make this a true pydantic schema and add a response type for if the status code is invalid).
    """
    id: int
    status_code: int
    oop_max: int
    remaining_oop_max: int
    copay: int
