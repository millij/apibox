#!flask/bin/python

import logging as log
import cgi
from flask import Flask, jsonify, make_response, abort, request, render_template, url_for
from multiprocessing import Process

# Mock_rest Requirements
from apibox.server import AppContainer, apps as a, launch_app_server_from_ui,app_content as aa
from apibox.mock_rest import *
#from flask.ext.cache import Cache
# Schema Validator
from apibox.utils.schema_validator import *
from werkzeug import secure_filename

import subprocess as sub
import os
import multiprocessing as mp
import json
import ast


def send_mr_obj(app_name):
    k = aa.get(str(app_name))
    return k
def conver_mockrestobj_to_dict(mockrest_obj):
    temp_list_endpoints = []
    for end_p in mockrest_obj.endpoints:
        if isinstance(end_p,EndPoint):
            temp_list_endpoints.append(end_p.__dict__)
        else:
            temp_list_endpoints.append(end_p)
    return temp_list_endpoints

class UIServer(object):

    'UI Server object'

    port = 8000               # Default UI Server Port

    app = Flask(__name__, static_folder='static')

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
        return render_template('indexnew.html')


    @app.route("/app/<app_name>", methods=["GET", "POST", "PUT", "DELETE"])
    def app_handler(app_name):
        """
        Applications handler
        """
        #print " I am in /app/<app_name> url"
        if request.method == 'GET':
            print " In GET"
            if aa.has_key(str(app_name)):
                mockrest_obj = send_mr_obj(app_name)
                temp_obj  = mockrest_obj.get_endpoints()
                app_details = mockrest_obj.get_app_details()
                return json.dumps(dict({"endpoints":temp_obj}.items()+app_details.items()))
            else:
                return "This app is not defined"

        elif request.method == 'POST':
            # POST: Create new App
            print "This Is POST Method"
            if app_name not in apps:
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
            file_type = "get the file type here"
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
                del aa[str(app_name)]
            except:
                print "No such app"

    @app.route("/app", methods=["GET", "POST", "PUT", "DELETE"])
    def app_new_handler():
        """
        Applications handler
        """
        print "In /app/new url"
        if request.method == 'POST':
            print " this is in post"
            file = request.files["filehere"]
            filename = secure_filename(file.filename)
            working_dir = os.path.join(os.getcwd()+"/uploadedfiles",filename)
            file.save(working_dir)
            is_valid, content = validate_file_content(
                working_dir, "JSON")
            if not is_valid:
                return "there is no content"
            aa.update({filename:MockREST.from_json(content)})
            print aa, " this is aa"
            mockrest_obj = send_mr_obj(filename)
            endpoints = conver_mockrestobj_to_dict(mockrest_obj)
            return render_template("indexnew.html",endpoints = endpoints)
            #return render_template("indexnew.html", aa=aa)
        return "reached new app"

    @app.route("/app/<app_name>/start", methods=["GET"])
    def app_handler_start(app_name):
        """
        Starts the app with the given name
        """
        port_number = 9999

        sub.call('ls', shell=True)
        kk = sub.call(
            'nohup python apibox/ui/sampleapp.py ' +
            str(app_name) +
            ' ' +
            str(port_number) +
            ' ' +
            '"test/kk.json" &> /dev/null &',
            shell=True)
        print "started the server "
        print (kk)
        return "successfully started the sever"

    @app.route("/app/<app_name>/stop", methods=["GET"])
    def app_handler_stop(app_name):
        """
        Stops the app with the given name
        """
        port_number = "get the port number"
        sub.call("fuser -k " + str(port_number) + "/tcp")

    @app.route(
        "/app/<app_name>endpoints",
        methods=[
            "GET",
            "POST",
            "PUT",
            "DELETE"])
    def app_endpoint_handler(app_name):
        """
        Applications endpoints handler
        :param app_name: Unique name of the application
        """
        if request.method == 'GET':
            # GET: Return endpoint details
            print "GET"
            print aa, "  this is aa in GET "
            mockrest_obj = send_mr_obj(app_name)
            endpoints = conver_mockrestobj_to_dict(mockrest_obj)
            return render_template("indexnew.html",endpoints = endpoints)
            #return json.dumps(conver_mockrestobj_to_dict(mockrest_obj))
        elif request.method == 'POST':
            try:
                temp_dict = ast.literal_eval(request.data)
                endpoint_obj = EndPoint.from_json(temp_dict)
            except:
                return " Invalid data"
            if aa.has_key(str(app_name)):
                mockrest_obj = send_mr_obj(app_name)
                if endpoint_obj.path in mockrest_obj.get_endpoints().values():
                    return " Already this endpoint exists"
                else:
                    mockrest_obj.add_endPoint(endpoint_obj)
                    print type(endpoint_obj), " this is endpoint_obj type in post"
                    print endpoint_obj.__dict__, " trying to convert endpoint_obj to dict"
                    aa[app_name] = mockrest_obj
                    for end_p in mockrest_obj.endpoints:
                        print type(end_p), " this is type od end_p in post method"
                    return " Successfully added new end point"
            else:
                print "Invalid AppName"

        elif request.method == 'PUT':
            # PUT: Update the endpoint
            print "PUT"
            path = "get the new end point here"
            method = "get the new method here"

            new_ep_obj = EndPoint(path, method)
            MockREST.add_endPoint(new_ep_obj)

        else:
            # DELETE: Delete the endpoint
            path = request.data
            mockrest_obj = send_mr_obj(app_name)
            if path in mockrest_obj.get_endpoints().values():
                endpoint_obj = mockrest_obj.get_endpoint(path)
                mockrest_obj.remove_endPoint(endpoint_obj)
                return "Successfuly deleted required end point"
            else:
                return " invalid end point"

    """ Routes / error handling """

    @app.errorhandler(404)
    def page_not_found(error):
        return make_response(jsonify({'error': 'Page Not found'}), 404)

    @app.errorhandler(500)
    def internal_server_error(error):
        return make_response(jsonify({'error': str(error)}), 500)
