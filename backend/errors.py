import json

class BaseError(Exception):
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

class UnexpectedError(BaseError):
    """
    Raise an unexpected error as our base error
    """
    def __init__(self, message="UnexpectedError"):
        self.message = message

class NotEnoughDataError(BaseError):
    """
    Raised when not enough copay data was returned to smooth out
    """
    def __init__(self, total_sent, total_received):
        self.total_sent: int = total_sent
        self.total_recieved: int = total_received
        self.message = f"Not enough data: {total_sent =}, {total_received = }" 

class BadDataError(BaseError):
    """
    If we want to we can extend our errors classes to handle more and more errors.

    For example, if all the servers are returning mangled data (due to an API change or something)
    """
    def __init__(self, bad_data):
        self.bad_data = bad_data
        self.message = "Unexpectedly bad data was recieved from the API endpoint"
