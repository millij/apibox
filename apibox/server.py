
from apibox.mock_rest import *

class MockRESTServer(object):
    'defines a mock rest server'

    default_host = 0.0.0.0
    default_port = 5000

    def __init__(self, mock_rest, host, port):
        """
        default constructor
        """
        if not isinstance(mock_rest, MockREST):
            raise TypeError("Invalid type. expected MockREST")

        self.mock_rest = mock_rest
        self.host = host or MockRESTServer.default_host
        self.port = port or MockRESTServer.default_port

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__


def launch_api_mock_server(host, port, mock_rest):
    """
    Launches a new mock rest server with the passed configuration. 
    """
    pass
