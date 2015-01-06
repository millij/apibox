
"""
This Module holds the definitions of MOCK REST objects.
"""

class MockRESTBase(object):

    def __json__(self):
        """
        exports the current MockREST object to JSON.
        """
        import json
        return json.dumps(self.__dict__, sort_keys=True)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__



class EndPointMethod(MockRESTBase):
    """
    defines a specific method of an endpoint. An endpoint with the same path
    can have have multiple request method types
    """

    def __init__(self, method, inp_data, result):
        """
        Default constructor.
        :param method: Request method type
        :param np_data: inp request data/body (if any)
        :param result: The result of the request
        """
        self.method = method
        self.inp_data = inp_data
        self.result = result

    def is_input_valid(self, in_data):
        """
        Validates the input data.
        :param in_data: incoming data.
        :return: True if the incoming data is valid and acceptible.
        """
        # TODO validator logic
        return True



class EndPoint(MockRESTBase):
    'Defines a REST endpoint'

    def __init__(self, path, methods):
        """
        default constructor. 
        :param path: REST endpoint path
        :param methods: an array of objects of type - EndPointMethod
        """
        if not path or path.isspace():
            raise ValueError("Invalid Path")

        self.path = path
        self.methods = methods or []

    def add_method(self, ep_method):
        """
        Adds new endpoint_method to the existing list.
        :param ep_method: EndPointMethod object
        """
        if not isinstance(ep_method, EndPointMethod):
            raise TypeError("Invalid type. expected EndPointMethod")

        self.methods.append(ep_method)

    def remove_method(self, ep_method):
        """
        Removes existing endpoint_method from the existing list.
        :param ep_method: EndPointMethod object
        """
        if not isinstance(ep_method, EndPointMethod):
            raise TypeError("Invalid type. expected EndPointMethod")

        try:
            self.methods.remove(ep_method)
        except ValueError as err:
            # log TypeError
            pass



class MockREST(MockRESTBase):
    'Defines a mock rest object. Includes all its end-points definitions.'

    def __init__(self, name, version, prefix, endpoints):
        """
        default constructor
        :param name: Name of the application.
        :param version: Version details of API (if any).
        :param prefix: Common prefix to prepend to all API paths (if any).
        :param endpoints: array of Mock API endpoints.
        """
        if not name or name.isspace():
            raise ValueError("Invalid Name")

        self.name = name
        self.version = version
        self.prefix = prefix or ""
        self.endpoints = endpoints or []

    def add_endPoint(self, ep):
        """
        Adds new endpoint to the the list of existing endpoints
        :param endpoint: EndPoint object
        """
        if not isinstance(ep, EndPoint):
            raise TypeError("Invalid type. expected EndPoint")

        self.endpoints.append(ep)

    def remove_endPoint(self, ep):
        """
        Removes the endpoint from the the list of existing endpoints
        :param endpoint: EndPoint object
        """
        if not isinstance(ep, EndPoint):
            raise TypeError("Invalid type. expected EndPoint")

        try:
            self.endpoints.remove(ep)
        except ValueError as err:
            # log TypeError
            pass



