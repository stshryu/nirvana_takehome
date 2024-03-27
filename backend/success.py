class Success:
    """
    Base object used for a successful request

    Attributes:
        response    -- The object to be successfully returned
    """
    def __init__(self, response):
        self.response = response

    """
    Method to unpack the success object into a result
    """
    def unpack(self):
        return self.response
