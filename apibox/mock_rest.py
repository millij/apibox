
"""
This Module holds the definitions of MOCK REST objects.
"""

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MockRESTBase(object):
    'Base class for Mock REST API classes'

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

    @classmethod
    def from_json(method_json):
        self.method = method_json.get("method")
        self.inp_data = method_json.get("inp_data")
        self.result = method_json.get("result")

	def get_result(self):
		return self.result
	

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

    @classmethod
    def from_json(endpoint_json):
        self.path = endpoint_json.get("path")
        self.methods = endpoint_json.get("methods")


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
            logger.debug(err)

    def get_method(self, in_method_type):
        """
        Returns the Method with the given type
        :param in_method_type: request method type
        """
        try:
            for method in self.methods:
                print str(self.methods),type(self.methods)
                if method.keys().contains(in_method_type):
                    return method.get(in_method_type)
                else:
                        return "not a valid method"		
        except Exception, e:
            print e


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

    @classmethod
    def from_json(mock_rest_json):
        self.name=mock_rest_json.get("name")
        self.version = mock_rest_json.get("version")
        self.prefix = mock_rest_json.get("prefix")
        self.endpoints = mock_rest_json.get("endpoints")


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

    def get_endpoint(self, in_path):
        """
        Returns the endpoint with the given path
        :param in_path: path of the endpoint
        """
        for end_p in self.endpoints:
            print type(end_p), " this is end_p"
            print end_p.get_method("path"), " this is path"
            if end_p.get_method("path")==in_path:
                return end_p
            else:
                return "not a valid path"



class MockRESTServer(MockRESTBase):
    'defines a mock rest server'

    default_host ='0.0.0.0'
    default_port = 5000

    def __init__(self, mock_rest, host, port):
        """
        default constructor
        :param mock_rest: object containing all the MockAPI details.
        :param host: host to start the server at.. (default: 0.0.0.0)
        :param port: port to start the server at.. (default: 5000)  
        """
        if not isinstance(mock_rest, MockREST):
            raise TypeError("Invalid type. expected MockREST")

        self.mock_rest = mock_rest
        self.host = host or MockRESTServer.default_host
        self.port = port or MockRESTServer.default_port


    def process_request(self, path, method, inp_data):
        pass


