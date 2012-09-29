from django.test import client

class Client(client.Client):
    """
    Test client which does not specially handle exceptions.

    Useful for testing HTTP 500 error handlers.
    """

    def store_exc_info(self, **kwargs):
        pass
