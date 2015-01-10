#!flask/bin/python

import logging as log
import json
from flask import Flask, jsonify, make_response, abort, request, render_template, url_for
from multiprocessing import Process

# Mock_rest Requirements
from apibox.server import AppContainer, apps as a
from apibox.mock_rest import *
#from flask.ext.cache import Cache
# Schema Validator
from apibox.utils.schema_validator import *
from werkzeug import secure_filename
import shelve
import subprocess as sub

import multiprocessing as mp
import ast

stopped_apps = shelve.open("stopped.txt", writeback=True)

def send_mr_obj(app_name):
    k = a[str(app_name)]
    is_valid, content = validate_file_content(str(k), "JSON")
    mock_rest = MockREST.from_json(content)
    kk = str(mock_rest.endpoints)
    return mock_rest


def send_mr_content(app_name):
    k = a[str(app_name)]
    is_valid, content = validate_file_content(str(k), "JSON")
    if is_valid:
        return content

class UIServer(object):

    'UI Server object'

    port = 5123               # Default UI Server Port
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

    @app.route("/", methods=["GET"])
    def apps_home():
        """
        Return all existing apps as JSON
        """
        # return "hi ths is kanth"
        return render_template('index.html', a=a,st=stopped_apps)

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
            except:
                print "No such app"

    @app.route("/app/new", methods=["GET", "POST", "PUT", "DELETE"])
    def app_new_handler():
        """
        Applications handler
        """
        if request.method == 'POST':
            import uuid

            app_name = str(uuid.uuid4())
            file = request.files["filehere"]
            file.save(os.path.join(str(app_name) + ".json"))
            is_valid, content = validate_file_content(
                str(app_name) + ".json", "JSON")
            if not is_valid:
                return "there is no content"
            mock_rest = MockREST.from_json(content)
            a[str(mock_rest.name)] = app_name +".json"
            return render_template("index.html", a=a, st=stopped_apps)
        return "reached new app"

    @app.route("/app/new_ui", methods=["POST"])
    def app_new_ui_handler():
        """
        Applications handler
        """
        if request.method == 'POST':

            print str(request.data)
            import uuid
            d ={}
            app_name = str(uuid.uuid4())
            d['name'] = str(request.form["name"])
            d['prefix'] = str(request.form["name"])
            d['version'] = str(request.form["name"])
            d['endpoints'] = []
            f = open(app_name+'.json','wb')
            import json
            json.dump(d, f)
            f.close()
            is_valid, content = validate_file_content(
                str(app_name) + ".json", "JSON")
            if not is_valid:
                return render_template("index.html", a=a, st=stopped_apps, status="Something Went wrong")
            mock_rest = MockREST.from_json(content)
            a[str(mock_rest.name)] = app_name +".json"
            return render_template("index.html", a=a, st=stopped_apps, status="Successfully Created <"+d['name']+">")
        return "reached new app"

    @app.route("/app/start/<app_name>", methods=["POST"])
    def app_handler_start(app_name):
        """
        Starts the app with the given name
        """
        if request.method=="POST":
            del stopped_apps[str(app_name)]
            return render_template("index.html", a=a, st=stopped_apps)


    @app.route("/app/stop/<app_name>", methods=["POST"])
    def app_handler_stop(app_name):
        """
        Stops the app with the given name
        """
        if request.method=="POST":
            print "Stopping the service"
            stopped_apps[str(app_name)] = 'stopped'
            return render_template("index.html", a=a, st=stopped_apps)

    @app.route(
        "/app/<app_name>/endpoint",
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
            kk = send_mr_obj(app_name)
            k = {}
            count =0
            for ep in kk.endpoints:
                k[count] = (dict(ep)['path'])
                count+=1
            return jsonify(k)

        elif request.method == 'POST':
            print (request.form), " this is request data"
            data= {}
            app_name = str(app_name)
            filename = a[app_name]

            # for container
            path = str(request.form['path'])
            mthd_type = str(request.form['method'])
            mthd_result = str( request.form['response'])

            ep_mthd = EndPointMethod(mthd_type, None, mthd_result)
            ep = EndPoint(path, None)
            ep.add_method(ep_mthd)
            # return ep.__str__()
            log.info(ep)
            log.info(ep.methods)

            # JSON file

            data['path'] =str(request.form['path'])
            data["methods"] = {'method': str(request.form['method']), 'result': str( request.form['response'])}

            import json
            if a.has_key(app_name):
                f = open(filename)
                la = json.load(f)
                print type(la['endpoints']), "Type of endpoints"
                print type(data), "type of data"
                # return str(len(la['endpoints']))

                la['endpoints'].append(data)

                mr_data= send_mr_obj(app_name)
                mr_data.add_endPoint(ep)

                log.info(str(la))
                # return mr_data.__str__()
                print la,"hey man"
                f.close()
                f = open(filename,'wb')
                json.dump(la, f)
                f.close()
                # f.write(json.load(f.read())['endpoints'].append(data))
                f.close()
                return render_template("index.html", a=a, st=stopped_apps,status="Sucessfully added <"+data["path"]+"> endpoint to <"+str(app_name)+">" )
                # return jsonify({'Success':data['path']})
            else:
                print "Invalid End point"

        elif request.method == 'PUT':
            # PUT: Update the endpoint
            print "PUT"
            path = "get the new end point here"
            method = "get the new method here"

            new_ep_obj = EndPoint(path, method)
            MockREST.add_endPoint(new_ep_obj)
            return ""


        else:
            # DELETE: Delete the endpoint
            enp_no = request.form['endpoint_no']

            log.info(str(enp_no)+" want to delete this one!!!")
            kk = send_mr_obj(app_name)
            k = {}
            count =0
            for ep in kk.endpoints:
                k[count] = (dict(ep)['path'])
                count+=1
            import json
            filename =a[app_name]
            f = open(filename)
            la = json.load(f)
            del la["endpoints"][int(enp_no)]
            log.info(str(la))
            f.close()
            f = open(filename,'wb')
            json.dump(la, f)
            f.close()
            # f.write(json.load(f.read())['endpoints'].append(data))
            f.close()
            del k[int(enp_no)]
            return jsonify(k)

    @app.route('/<path:path>', methods=["GET", "POST", "DELETE", "PUT"])
    def catch_all(path):
        print path

        app_name = str(path.split('/')[0])
        pathd = str(path.replace(app_name,''))

        print
        print
        print app_name, pathd
        if a.has_key(app_name) and not stopped_apps.has_key(app_name):
            # return render_template("index.html", a=a, st=stopped_apps)
            # code to get the end point result from json file
            print "coming to path route"

            end_points_result=send_mr_obj(app_name).get_endpoint(pathd,str(request.method))

            return end_points_result.__str__()
        else:
            return jsonify({'error': 'This App is Currently Disabled'})

    """ Routes / error handling """

    @app.errorhandler(404)
    def page_not_found(error):
        return make_response(jsonify({'error': 'Page Not found'}), 404)

    @app.errorhandler(500)
    def internal_server_error(error):
        return make_response(jsonify({'error': str(error)}), 500)
