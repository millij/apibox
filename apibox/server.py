
from apibox.mock_rest import *




def launch_api_mock_server(host, port, mr_json):
    """
    Launches a new mock rest server with the passed configuration.
    """

    mock_rest_obj = MockREST.from_json(mr_json)

    # add to the app container (singleton) dictionary.
    
    # start the server
    

    pass
