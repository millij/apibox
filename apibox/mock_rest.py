
"""
This Module holds the definitions of MOCK REST objects.
"""

class EndPointMethod(object):
    """
    defines a specific method of an endpoint. An endpoint with the same path
    can have have multiple request method types
    """

    def __init__(self, method, inp_data, result):
        """
        Default constructor.
        method: Request method type
        inp_data: inp request data/body (if any)
        result: The result of the request
        """
        self.method = method
        self.inp_data = inp_data
        self.result = result

    def is_input_valid(self, data):
        """
        Validates the input data.
        """
        pass


class Endpoint(object):
    'Defines a REST endpoint'

    def __init__(self, path, methods):
        """
        default constructor. 
        path: REST endpoint path
        methods: an array of objects of type - EndPointMethod
        """
        self.path = path
        self.methods = methods

    def add_endPointMethod(self, ep_method):
        """
        endpoint: Endpoint object
        Adds new endpoint to the the list of existing endpoints
        """
        pass



class MockREST(object):
    'Defines a mock rest object. Includes all its end-points definitions.'

    def __init__(self, name, version, prefix, endpoints):
        """
        default constructor
        """
        self.name = name
        self.version = version
        self.prefix = prefix
        self.endpoints = endpoints


    def add_endPoint(self, endpoint):
        """
        endpoint: Endpoint object
        Adds new endpoint to the the list of existing endpoints
        """
        pass

    def export_as_json(self):
        """
        exports the current MockREST object to JSON.
        """
        pass


