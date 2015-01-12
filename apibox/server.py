
from utils.schema_validator import *
import shelve

from mock_rest import *
# from flask.ext.cache import Cache
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from flask import Flask, request, render_template
from mock_rest import *

import multiprocessing as mp
# TODO: make configurable files


class AppContainer(object):
    pass

apps = shelve.open("allapps.txt", writeback=True)
#app_content = shelve.open("allcontent.txt",writeback=True)
app_content = {}


def add_app(app_name, mock_rest):
    global apps
    apps.update({app_name: mock_rest})


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

        #launch_flask_server(port, mock_rest)

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
    :type port: integer
    """
    app_name = mock_rest.name

    # cache = Cache(config={'CACHE_TYPE': 'simple'})

    app = Flask(str(mock_rest.name).replace(" ", ''), static_folder='static')
    # cache.init_app(app)
    # print app
    # print port,"his is prot"
    #@app

    @app.route('/Apibox')
    def index():
        """ Displays the index page accessible at '/Apibox'
        """

        return render_template('index.html')

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>', methods=["GET", "POST", "DELETE", "PUT"])
    def catch_all(path):
        path = "/" + path

        endpoint_obj = mock_rest.get_endpoint(path, request.method)
        return str(endpoint_obj)
        # print path, " this is path"
        #print (mock_rest.endpoints),"is it mock rest object"
        endpoint_obj = mock_rest.get_endpoint(path)
        if isinstance(endpoint_obj, str):
            return endpoint_obj.__json__()
        else:
            method = endpoint_obj.get_method(request.method)
            if isinstance(method, str):
                return method
        return str(method.get_result())

    if not shut_down:
        app.run(debug=True, port=port)
