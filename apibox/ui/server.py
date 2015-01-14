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
import urllib
WELCOME = "Welcome to Mocking Bird. Create your API's here and render them outside"
API_EDIT = "Your Endpoint is Updated: "
API_DELETE = "Your Endpoint is Deleted: "
API_CREATE = "Your Endpoint is Created:  "
API_START = "Your Endpoint is Available: "
API_STOP = "Your Endpoint is Halted: "


stopped_apps = shelve.open("stopped.txt", writeback=True)
endpoint_status = shelve.open("stopped_endpoints.txt", writeback=True)
ep_method_status = shelve.open('stopped_methods.txt',writeback=True)

file_type="JSON"

def get_content(app_name):
    path=a[str(app_name)]
    is_valid,content=validate_file_content(str(path),file_type)
    if is_valid:
        return content
    
def get_mock_obj(app_name):
    mock_rest = MockREST.from_json(get_content(app_name))
    kk = str(mock_rest.endpoints)
    return mock_rest

def get_endpts_methods(app_name):
    content=get_content(app_name)
    for datal in content['endpoints']:
        all_method = []
        for method in datal["methods"]:
            all_method.append(dict(method)['method'])
        ep_method_status[str(dict(datal)['path'])] = all_method
    return ep_method_status

def getresult(app_name, endpoint, method):
    content =get_content(app_name)
    for data in content['endpoints']:
        if endpoint == dict(data)['path']:
            methods = (dict(data)['methods'])

            for me in methods:
                if method == dict(me)['method']:
                    return dict(me)['result']
    return False

def send_endpoints(app_name):
    content=get_content(app_name)
    rest = get_endpts_methods(app_name)

    if rest:
        for data in content['endpoints']:
            path_name = str(dict(data)['path'])
            endpoint_status[str(dict(data)['path'])] = 'started^'+str(app_name)+'$'+','.join(ep_method_status[str(path_name)])
        return True

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
        return render_template('index.html', a=a,st=stopped_apps, ste = endpoint_status, status= WELCOME)

    # @cache.cached(timeout=None)

    @app.route("/app/<app_name>", methods=["GET", "POST", "PUT", "DELETE"])
    def app_handler(app_name):
        """
        Applications handler
        """
        if request.method == 'GET':
            # GET: Return app details
            print "GET"
            kk = get_mock_obj(app_name)
            return (json.dumps(kk.endpoints))

        elif request.method == 'POST':
            # POST: Create new App
            print "This Is POST Method"
            if app_name not in apps:
                print (request.data), " this is request data"
                temp_dict = ast.literal_eval(request.data)
                mockrest_obj = MockREST.from_json(temp_dict)
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

    @app.route("/app/new", methods=["GET", "POST"])
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
            if  send_endpoints(str(mock_rest.name)):
                return render_template("index.html", a=a, st=stopped_apps, ste = endpoint_status, status = "Successfully Created New App", status_app=str(mock_rest.name))
            return render_template("index.html", a=a, st=stopped_apps, ste = endpoint_status, status= "Something Wrong with your Config File")
        return "reached new app"



    # Useless in the Kavitas model of UI

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
            return render_template("index.html", a=a, st=stopped_apps, status="Successfully Created New App ", status_app=d['name'])
        return "reached new app"

    @app.route("/app/start/<app_name>", methods=["POST"])
    def app_handler_start(app_name):
        """
        Starts the app with the given name
        """
        if request.method=="POST":
            del stopped_apps[str(app_name)]
            return render_template("dd/static/index.html", a=a, st=stopped_apps)


    @app.route("/app/stop/<app_name>", methods=["POST"])
    def app_handler_stop(app_name):
        """
        Stops the app with the given name
        """
        if request.method=="POST":
            print "Stopping the service"
            stopped_apps[str(app_name)] = 'stopped'
            return render_template("index.html", a=a, st=stopped_apps)




    @app.route("/start/<app_name>/path", methods=["POST"])
    def ep_handler_start(app_name):
        """
        Starts the app endpoint with the given name
        """
        app_name =str(app_name)
        path = str(request.form['path'])
        if request.method=="POST":
            endpoint_status[path] = "started^"+app_name+'$'+','.join(ep_method_status[str(path)])
            if path.startswith('/'):
                path = '/'+app_name+''+path
            path = '/'+app_name+'/'+path
            return render_template("index.html", a=a, st=stopped_apps ,ste=endpoint_status, status=API_START, status_url=path)


    @app.route("/stop/<app_name>/path", methods=["POST"])
    def ep_handler_stop(app_name):
        """
        Stops the app's endpoint with the given name
        """
        print "I'm at stopping path"
        app_name =str(app_name)
        path = str(request.form['path'])
        if request.method=="POST":
            print "Stopping the service"
            endpoint_status[path] = "stopped^"+app_name+'$'+','.join(ep_method_status[str(path)])
            if path.startswith('/'):
                path = '/'+app_name+''+path
            path = '/'+app_name+'/'+path
            return render_template("index.html", a=a, st=stopped_apps, ste = endpoint_status, status=API_STOP, status_url=path)




    @app.route(
        "/app/<app_name>/endpoint",
        methods=[
            "GET",
            "POST",
            "DELETE"])
    def app_endpoint_handler(app_name):
        """
        Applications endpoints handler
        :param app_name: Unique name of the application
        """
        if request.method == 'GET':
            # GET: Return endpoint details
            print "GET"
            kk = get_mock_obj(app_name)
            k = {}
            count =0
            for ep in kk.endpoints:
                k[count] = (dict(ep)['path'])
                count+=1
            return jsonify(k)


    @app.route('/app/endpoint/newone',methods=['POST'])
    def ep_new_one():
        if request.method=="POST":
            print (request.form), " this is request data"
            data= {}
            app_name = str(request.form['appnames'])
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
            data["methods"] = []
            kk = {'method': str(request.form['method']), 'result': str( request.form['response'])}
            data["methods"].append(kk)
            print data["methods"],"this is the response"
            import json
            if a.has_key(app_name):
                f = open(filename)
                la = json.load(f)
                print type(la['endpoints']), "Type of endpoints"
                print type(data), "type of data"
                # return str(len(la['endpoints']))

                la['endpoints'].append(data)
                #
                # mr_data= get_mock_obj(app_name)
                # mr_data.add_endPoint(ep)

                log.info(str(la))
                # return mr_data.__str__()
                print la,"hey man"
                f.close()
                f = open(filename,'wb')
                json.dump(la, f)
                f.close()
                # f.write(json.load(f.read())['endpoints'].append(data))
                f.close()
                send_endpoints(app_name)
                if str(request.form['path']).startswith('/'):
                    path = str(app_name)+''+str(request.form['path'])
                path = str(app_name)+"/"+str(request.form['path'])
                return render_template("index.html", a=a, st=stopped_apps,status=API_CREATE, status_url=path, ste=endpoint_status )
                # return jsonify({'Success':data['path']})
            else:
                print "Invalid End point"



    @app.route('/app/<app_name>/changeep' ,methods=['POST'])
    def endpoint_change(app_name):
        if request.method=="POST":

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


            data['path'] =str(request.form['path'])
            data["methods"] = {'method': str(request.form['method']), 'result': str( request.form['response'])}

            import json
            if a.has_key(app_name):
                f = open(filename)
                la = json.load(f)
                # print type(la['endpoints']), "Type of endpoints"
                # print type(data), "type of data"
                # return str(len(la['endpoints']))
                count = 0
                for ddd in la['endpoints']:
                    count = count+1
                    if dict(ddd)['path'] == data['path']:
                        break
                c=0
                for some_mthd in la['endpoints'][int(count)-1]['methods']:
                    c +=1
                    if dict(some_mthd)['method'] == mthd_type:
                        break

                la['endpoints'][int(count)-1]['methods'][c-1]['result']=str(request.form['response'])

                print "here are the changed endpoints"
                print la['endpoints']
                #
                f.close()
                f = open(filename,'wb')
                json.dump(la, f)
                f.close()
                # f.write(json.load(f.read())['endpoints'].append(data))
                f.close()
                send_endpoints(str(app_name))
                if data['path'][0] =='/':
                    data['path'] = '/'+str(app_name)+''+data['path']
                data['path'] = '/'+str(app_name)+"/"+data['path']
                return render_template("index.html", a=a, st=stopped_apps,status=API_EDIT, status_url=data['path'], ste=endpoint_status )
                # return jsonify({'Success':data['path']})
            else:
                print "Invalid End point"

    @app.route('/app/path/delete',methods=['POST'])
    def delete_path():
        path = str(request.form['path'])
        app_name = str(request.form['appname'])
        print path, app_name
        f = open(str(a[app_name]))
        la = json.load(f)
        count = 0
        for ddd in la['endpoints']:
            count = count+1
            if dict(ddd)['path'] == path:
                break
        del la['endpoints'][count-1]
        del endpoint_status[path]
        del ep_method_status[path]
        print "deleted endpoint "+path
        f.close()

        f = open(str(a[app_name]),'wb')
        json.dump(la, f)
        f.close()
        send_endpoints(str(app_name))
        if path.startswith('/'):
            path = '/'+app_name+''+path
        path = '/'+app_name+'/'+path
        return render_template("index.html", a=a, st=stopped_apps,status=API_DELETE, status_url=path, ste=endpoint_status)
        # return jsonify({'Success':data['path']})


    @app.route('/<path:path>', methods=["GET", "POST", "DELETE", "PUT"])
    def catch_all(path):
        print path

        app_name = str(path.split('/')[0])
        pathd = str(path.replace(app_name,''))

        print
        print
        print app_name, pathd
        if a.has_key(app_name) and not stopped_apps.has_key(app_name):
            if endpoint_status[pathd].startswith('started'):
            # return render_template("index.html", a=a, st=stopped_apps)
            # code to get the end point result from json file
                print "coming to path route"

                # end_points_result=get_mock_obj(app_name).get_endpoint(pathd,str(request.method))
                result_data= getresult(app_name, pathd, str(request.method))
                return str(result_data)
            else:
                return jsonify({'error': 'This API is Currently Disabled'})


        else:
            return jsonify({'error': 'This App is Currently Disabled'})

    """ Routes / error handling """

    @app.errorhandler(404)
    def page_not_found(error):
        return make_response(jsonify({'error': 'Page Not found'}), 404)

    @app.errorhandler(500)
    def internal_server_error(error):
        return make_response(jsonify({'error': str(error)}), 500)
