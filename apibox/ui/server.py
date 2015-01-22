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


def convert_dict_obj(endpoints):
    temp_list = []
    for end_p in endpoints:
        if isinstance(end_p,EndPoint):
            temp_list.append(end_p)
        else:
            temp_list.append(EndPoint.from_json(end_p))
    return temp_list

def convert_dict_objmethod(methods):
    temp_list = []
    for method in methods:
        if isinstance(method,EndPointMethod):
            temp_list.append(method)
        else:
            temp_list.append(EndPointMethod(method.get("method"),"",method.get("result")))
    return temp_list

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
        #return render_template('indexnew.html')
        return render_template('second.html')


    @app.route("/app/<app_name>", methods=["GET", "POST", "PUT", "DELETE"])
    def app_handler(app_name):
        """
        Applications handler
        """
        #print " I am in /app/<app_name> url"
        if request.method == 'GET':
            print " In GET"
            if aa.has_key(str(app_name)):
                mockrest_obj = aa.get(str(app_name))
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
    @app.route("/endpoint", methods = ["GET","POST","PUT","DELETE"])
    def app_addendpoint_holder():
        if request.method == "POST":
            path = request.form["path"]
            method = request.form["method"]
            response = request.form["response"]
            app_name = path.split("/")
            endpoint_path = path.replace(app_name[0],"",1)
            mockrest_obj = aa.get(str(app_name[0]))
            endpoint_obj = mockrest_obj.get_endpoint(endpoint_path)
            if endpoint_obj.check_method(method):
                endpoint_obj.update_method(method,response)
            else:
                endpoint_obj.add_method(EndPointMethod(method,"",response))
            return render_template("indexnew.html",mockrest_obj_list = aa.values(),app_names = aa.keys())
        else:
            return "Hello"
    @app.route("/endpoint_details", methods = ["POST"])
    def endpoint_details():
        app_name = request.form["app_name"]
        endpoint_path = request.form["endpoint_path"]
        mockrest_obj = aa.get(str(app_name))
        endpoint_obj = mockrest_obj.get_endpoint(endpoint_path)
        return render_template("tables.html",methods = convert_dict_objmethod(endpoint_obj.methods))

    @app.route("/addendpoint", methods=["POST"])
    def app_new_holder():
        app_name = request.form["appname"]
        endpoint_path = request.form["path"]
        method = request.form["method"]
        response = request.form["response"]
        mockrest_obj = aa.get(str(app_name))
        endpoint_obj = EndPoint(endpoint_path,[{"method":method,"result":response}])
        mockrest_obj.add_endpoint(endpoint_obj)
        return render_template("indexnew.html",mockrest_obj_list = aa.values(),app_names = aa.keys())
            
                    
    @app.route("/delete_endpoint", methods = ["POST"])
    def delete_endpoint():
        app_name = request.form["app_name"]
        endpoint_path = request.form["endpoint_path"]
        mockrest_obj = aa.get(str(app_name))
        mockrest_obj.remove_endpoint(endpoint_path)
        return render_template("indexnew.html",mockrest_obj_list = aa.values(),app_names =aa.keys())
        
    @app.route("/app", methods=["POST"])
    def app_new_handler():
        """
        Applications handler
        """
        print "In /app url"
        file = request.files["filehere"]
        filename = secure_filename(file.filename)
        working_dir = os.path.join(os.getcwd()+"/uploadedfiles",filename)
        file.save(working_dir)
        is_valid, content = validate_file_content(
            working_dir, "JSON")
        if not is_valid:
            return "there is no content"
        mockrest_obj = MockREST.from_json(content)
        aa.update({mockrest_obj.name:mockrest_obj})
        app_names = aa.keys()
        return render_template("indexnew.html",mockrest_obj_list = aa.values(),app_names = aa.keys())
        
    @app.route("/app1",methods = ["POST"])
    def new_app_form():
        print " in /app1 url"
        app_name = request.form["app_name"]
        path = request.form["endpoint_path"]
        method = request.form["method"]
        response = request.form["response"]
        methods = [{"method":method,"result":response}]
        endpoints = [{"path":path,"methods":methods}]
        mockrest_obj = MockREST(app_name,app_name,app_name,endpoints)
        aa.update({mockrest_obj.name:mockrest_obj})
        return render_template("indexnew.html",mockrest_obj_list = aa.values(),app_names = aa.keys())

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
        "/app/<app_name>/endpoints",
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
            mockrest_obj = aa.get(str(app_name))
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
                mockrest_obj = aa.get(str(app_name))
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
            mockrest_obj = aa.get(str(app_name))
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
