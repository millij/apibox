#!flask/bin/python

import logging as log

from flask import Flask, jsonify, make_response, abort, request
from multiprocessing import Process

# Mock_rest Requirements
from apibox.server import AppContainer, apps as a, launch_app_server_from_ui
from apibox.mock_rest import *

# Schema Validator
from apibox.utils.schema_validator import *

class UIServer(object):
    'UI Server object'

    port = 8000               # Default UI Server Port 
    app = Flask(__name__)

    def __init__(self):
        print "UI server Initiated"
        pass

    def start(self):
        print "Starting ui server ... "
        UIServer.app.run(debug=True, port=UIServer.port)
        print "UI Server started successfully"

    def stop(self):
        print "Stopping ui server ... "
        # TODO
        print "UI Server stopped successfully"


    """ Routes for UI Support """

    @app.route("/", methods=["GET"])
    @app.route("/app", methods=["GET"])
    def apps_home():
        """
        Return all existing apps as JSON
        """

        return "hi here is the length of apps "

    @app.route("/app/<app_name>", methods=["GET", "POST", "PUT", "DELETE"])
    def app_handler(app_name):
        """
        Applications handler
        """

        if request.method == 'GET':
            # GET: Return app details
            print "GET"
            return a.keys()

        elif request.method == 'POST':
            # POST: Create new App
            print "POST"
            file_path = "get the file path here from form"
            file_type= "get the file type here"
            is_valid, content = validate_file_content(file_path, file_type)
            if not content is None:
                mock_rest = MockREST.from_json(content)
                a[app_name] = mock_rest
                return "Created New App"
            return "Config file is not valid"

        elif request.method == 'PUT':
            # PUT: Update the App
            print "PUT"
            file_path = "get the path here"
            file_type= "get the file type here"
            is_valid, content = validate_file_content(file_path, file_type)
            if not content is None:
                mock_rest = MockREST.from_json(content)
                a[app_name] = mock_rest
                return "Updated New App"
            return "Config file is not valid"
        else:
            # DELETE: Delete the APP
            print "DELETE"
            try:
                del a[app_name]
            except:
                print "No such app"




    @app.route("/app/<app_name>/start", methods=["GET"])
    def app_handler_start(app_name):
        """
        Starts the app with the given name
        """
        port_number = "get the port number"

        launch_app_server_from_ui(port_number, a[app_name])
        return "successfully started the sever"


    @app.route("/app/<app_name>/stop", methods=["GET"])
    def app_handler_stop(app_name):
        """
        Stops the app with the given name
        """
        pass


    @app.route("/app/<app_name>/endpoint", methods=["GET", "POST", "PUT", "DELETE"])
    def app_endpoint_handler(app_name):
        """
        Applications endpoints handler
        :param app_name: Unique name of the application
        """
        if request.method == 'GET':
            # GET: Return endpoint details
            print "GET"
            return AppContainer.get_app(app_name)
        elif request.method == 'POST':
            # POST: Create new endpoint
            print "POST"
            ep_name = "get the file name here from form"
            method_name = "get method name"
            input_data = "get data here"
            reuslt = "get result for the method"
            ep_meth   =  EndPointMethod(method_name, input_data, result)
            new_ep_obj = EndPoint.add_method(ep_meth)

        elif request.method == 'PUT':
            # PUT: Update the endpoint
            print "PUT"
            path = "get the new end point here"
            method = "get the new method here"

            new_ep_obj = EndPoint(path, method)
            MockREST.add_endPoint(new_ep_obj)

        else:
            # DELETE: Delete the endpoint
            ep_path = "get the path here"
            ep_obj = MockREST.get_endpoint(ep_path)
            MockREST.remove_endPoint(ep_obj)
            print "DELETE"



    """ Routes / error handling """

    @app.errorhandler(404)
    def page_not_found(error):
        return make_response(jsonify({'error': 'Page Not found'}), 404)

    @app.errorhandler(500)
    def internal_server_error(error):
        return make_response(jsonify({'error': str(error)}), 500)





