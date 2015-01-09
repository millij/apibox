
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
app_objs = {}


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
        launch_flask_server(file_path, str(mock_rest.name))

        #launch_flask_server(port, mock_rest)

        # TODO Add these details to app container

    else:
        print "Invalid Content"
        raise ValueError("Invalid Content")

def launch_flask_server(fp, name):
    """
    Launches a new mock rest server with the passed configuration.

    """
    from apibox.ui.server import *
    import requests

    print "Starting Server...."
    UIServer().start()
    file_name =name
    print "Adding "+str(file_name)+ " to current API BOX"
    r = requests.post('http://127.0.0.1:5123/app/new', files={'filehere': open(fp, 'r')})
    a[name] = fp
    print "Added "+str(file_name)+ " to current API BOX"





