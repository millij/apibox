
from apibox.mock_rest import *
from apibox.utils.schema_validator import *
import shelve
from apibox.mock_rest import *
# from flask.ext.cache import Cache
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

#TODO: make configurable files

class AppContainer(object):
    pass

apps = shelve.open("allapps.txt",writeback=True)


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
        print type(mock_rest.name)
        apps[str(mock_rest.name)] = file_path
        launch_flask_server(port, mock_rest) 

        # TODO Add these details to app container

    else:
        print "Invalid Content"
        raise ValueError("Invalid Content")



def launch_app_server_from_ui(port, app_data):
    # launch server
    if app_data:
        launch_flask_server(port, app_data)
    else:
        print "Invalid Content"
        raise ValueError("Invalid Content")

def launch_flask_server(port, mock_rest, shut_down=False):
    """
    Launches a new mock rest server with the passed configuration.
    """
    app_name = mock_rest.name
    from flask import Flask, request
    # cache = Cache(config={'CACHE_TYPE': 'simple'})

    app = Flask(__name__)
    # cache.init_app(app)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>', methods=["GET", "POST", "DELETE", "PUT"])
    def catch_all(path):
        path = "/"+path
        endpoint_obj = mock_rest.get_endpoint(path, request.method)


        return str(endpoint_obj)
        # return str(method.get_result())
    if not shut_down:
#
# http_server = HTTPServer(WSGIContainer(app))
# http_server.listen(5000)
# IOLoop.instance().start()
        app.run(debug=True, port = port)
