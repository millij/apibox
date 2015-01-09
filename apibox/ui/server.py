#!flask/bin/python

import logging as log

from flask import Flask, jsonify, make_response, abort, request, render_template, url_for
from multiprocessing import Process

# Mock_rest Requirements
from apibox.server import AppContainer, apps as a, launch_app_server_from_ui
from apibox.mock_rest import *
#from flask.ext.cache import Cache
# Schema Validator
from apibox.utils.schema_validator import *
from werkzeug import secure_filename
<<<<<<< HEAD
import subprocess as sub
=======

>>>>>>> 8462dad99b5b949db0f48d8c6d253771f21d84f9
import multiprocessing as mp
import json
import ast

def send_mr_obj(app_name):
    k = a[str(app_name)]
    is_valid, content = validate_file_content(str(k), "JSON")
    mock_rest = MockREST.from_json(content)
    kk =  str(mock_rest.endpoints)
    return mock_rest

class UIServer(object):
    'UI Server object'


    port = 8000               # Default UI Server Port
    #cache = Cache(config={'CACHE_TYPE': 'simple'})

    UPLOAD_FOLDER = ''
    app = Flask(__name__, static_folder='static')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    #@cache.cached(timeout=None)
    @app.route("/", methods=["GET"])
    def apps_home():
        """
        Return all existing apps as JSON
        """
        # return "hi ths is kanth"
        return render_template('index.html',a=a)

    # @cache.cached(timeout=None)

    @app.route("/app/<app_name>", methods=["GET", "POST", "PUT", "DELETE"])
    def app_handler(app_name):
        """
        Applications handler
        """
        if request.method == 'GET':
            # GET: Return app details
            print "GET"
            kk = send_mr_obj(app_name)
            return (json.dumps(kk.endpoints))

        elif request.method == 'POST':
            # POST: Create new App
            print "This Is POST Method"
            if not apps.has_key(app_name):
                print (request.data), " this is request data"
                temp_dict = ast.literal_eval(request.data)
                mockrest_obj = MockREST.from_json(temp_dict)
                print mockrest_obj, " this is endpoint_obj"
                print type(mockrest_obj), " this is type of endpoint_obj"
                return str(mockrest_obj)
            else:
                return "Request app already has"

        elif request.method == 'PUT':
            # PUT: Update the App
            print "PUT"
            file_path = "get the path here"
            file_type= "get the file type here"
            is_valid, content = validate_file_content(file_path, file_type)
            if not content is None:
                mock_rest = MockREST.from_json(content)
                a[str(mock_rest.name)] = file_path
                return "Updated New App"
            return "Config file is not valid"
        else:
            # DELETE: Delete the APP
            print "DELETE"
            try:
                del a[app_name]
            except:
                print "No such app"

    @app.route("/app/new", methods=["GET", "POST", "PUT", "DELETE"])
    def app_new_handler():
        """
        Applications handler
        """
        if request.method == 'POST':
            app_name = request.form["app_name"]
            port_num = request.form["port_number"]
            print port_num
            file = request.files["filehere"]
            file.save(os.path.join(str(app_name)+".json"))
            is_valid, content = validate_file_content(str(app_name)+".json", "JSON")
            if not is_valid:
                return "there is no content"
            a[str(app_name)] = str(app_name)+".json$$"+str(port_num).strip()

            return render_template("index.html", a=a)
        return "reached new app"

    @app.route("/app/<app_name>/start", methods=["GET"])
    def app_handler_start(app_name):
        """
        Starts the app with the given name
        """
        port_number = 9999

        sub.call('ls',shell=True)
        kk = sub.call('nohup python apibox/ui/sampleapp.py '+str(app_name)+' '+str(port_number) +' '+ '"test/kk.json" &> /dev/null &', shell=True)
        print "started the server "
        print (kk)
        return "successfully started the sever"


    @app.route("/app/<app_name>/stop", methods=["GET"])
    def app_handler_stop(app_name):
        """
        Stops the app with the given name
        """
        port_number = "get the port number"
        sub.call("fuser -k "+str(port_number)+"/tcp")

    @app.route("/app/<app_name>/endpoint", methods=["GET", "POST", "PUT", "DELETE"])
    def app_endpoint_handler(app_name):
        """
        Applications endpoints handler
        :param app_name: Unique name of the application
        """
        if request.method == 'GET':
            # GET: Return endpoint details
            print "GET"
            kk = send_mr_obj(app_name)
            return str(kk.endpoints)
        elif request.method == 'POST':
            print (request.data), " this is request data"
            
            temp_dict = ast.literal_eval(request.data)
            endpoint_obj = EndPoint.from_json(temp_dict)
            if a.has_key(app_name):
                send_mr_obj(app_name).add_endPoint(endpoint_obj)
            else:
                print "Invalid End point"

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

