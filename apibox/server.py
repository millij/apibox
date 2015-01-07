from mock_rest import *

class AppContainer(object):

    apps = {}

    def __init__(self):
        pass

    def add_app(self, app_name, mock_rest):
        apps.update({app_name:mock_rest})

    def remove_app(self, app_name):
        del apps[app_name]

    def get_app(self, app_name):
        return apps.get(app_name)



def launch(host, port, mock_rest):
    """
    Launches a new mock rest server with the passed configuration.
    """
    app_name = mock_rest.name
    from flask import Flask, request
    app = Flask(app_name)
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>', methods=["GET", "POST", "DELETE", "PUT"])
    def catch_all(path):
        path = "/"+path
        endpoint_obj = mock_rest.get_endpoint(path)
        method = endpoint_obj.get_method(request.method)
        return str(method.get_result())

    app.run(debug=True,host = host,port = port)


