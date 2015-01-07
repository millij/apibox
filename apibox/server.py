
from apibox.mock_rest import *
from apibox.utils.schema_validator import *


class AppContainer(object):
    pass


from apibox.mock_rest import *

# Global app holder
apps = {}

def add_app(app_name, mock_rest):
    global apps
    apps.update({app_name:mock_rest})

def remove_app(app_name):
    global apps
    del apps[app_name]

def get_app(app_name):
    global apps
    return apps.get(app_name)



def launch_app_server_from_file(port, file_path, file_type):

    # validate and get the file content
    is_valid, content = validate_file_content(file_path, file_type)

    if is_valid:
        if(file_type == "JSON"):
            mock_rest = MockREST.from_json(content)

        # launch server
        launch_flask_server(port, mock_rest) 

        # TODO Add these details to app container

    else:
        print "Invalid Content"
        raise ValueError("Invalid Content")


def launch_flask_server(port, mock_rest):
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

    app.run(debug=True, port = port)


