from fastapi.testclient import TestClient
import pytest
from services.copay_retrieval_service import *
from httpx import Response
import asyncio
import success
import errors

valid_response = [
    Response(200, json={'status_code': 200, 'id': '1', 'oop_max': 10000, 'remaining_oop_max': 9000, 'copay': 1000}),
    Response(200, json={'status_code': 200, 'id': '1', 'oop_max': 20000, 'remaining_oop_max': 9000, 'copay': 50000}),
    Response(200, json={'status_code': 200, 'id': '1', 'oop_max': 10000, 'remaining_oop_max': 8000, 'copay': 1000}),
]

invalid_response = [
    Response(500, json={'status_code': 500, 'message': 'internal server error'}),
    Response(500, json={'status_code': 500, 'message': 'internal server error'}),
    Response(200, json={'status_code': 200, 'id': '1', 'oop_max': 10000, 'remaining_oop_max': 9000, 'copay': 1000})
]

def test_analyze_copay_data():
    # Arrange
    response = valid_response 

    # Act
    result = asyncio.run(analyze_copay_data(response))

    # Assert
    assert type(result) == success.Success

def test_analyze_copay_data_failure():
    # Arrange
    response = invalid_response

    # Act
    result = asyncio.run(analyze_copay_data(response))

    # Assert
    assert type(result) == errors.NotEnoughDataError

def test_percent_received():
    # Arrange
    total_sent = 30
    total_recieved = 28

    # Act
    result = asyncio.run(percent_recieved(total_sent, total_recieved))

    # Assert
    assert result is True

def test_percent_recieved_failure():
    # Arrange
    total_sent = 30
    total_recieved = 5

    # Act 
    result = asyncio.run(percent_recieved(total_sent, total_recieved))

    # Assert
    assert result is False

def test_smooth_data():
    # Arrange
    response = valid_response
    # We mock the data type we expect to pass into the data smoother. We could call analyze_copay_data() but that would create a dependency between the two functions in our test.
    data = [ CopayResponse(**i.json()) for i in response if i.json()['status_code'] == 200 ]

    # Act 
    result = asyncio.run(smooth_data(data))

    # Assert
    assert result["status"] == "success"

def test_notifier_queue():
    pass

def test_enqueue_copay_jobs():
    pass
