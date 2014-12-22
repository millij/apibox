from flask import Flask, jsonify, request, render_template, redirect, url_for
import json
import collections

def convert(data):
    ''' 
    converts json object to dictionary ( from unicode dict to dict )
    
    Input:

    - data: json object
    
    Output: dictionary

    '''
    
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


def url_methods(path, method,dict_of_json):
    '''
    takes path as url and method as one of the  methods and return the appropriate value

    Inputs:

    - path: endpoint path

    - method: enum value ["GET","POST","DELETE","PUT"], here this method is mostly for GET

    Return: appropriate value

    '''
    if method in dict_of_json[path][0]:
        return dict_of_json[path][0][method]["success"]
    else:
        return "This method is not supported"

#why try catch is expensive?


def create(file_name):
    '''
    Used to create vaiables for storing endpoints, prefixes and list of end points
    
    Inputs:

    - file_name: filename
    
    Returns: all the three variables.
    
    '''
    dict_of_json = {}   # temprary variable to store the json as dictionary
    list_endpoints_path = []    # list of all the endpoints mentioned by the user
    prefix_list = []    #stores name and version of the project mentioned by the user
    json_obj = json.load(open(file_name))
    temp = convert(json_obj)
    prefix_list.append(temp.get("name"))
    prefix_list.append(temp.get("version"))
    endpoints_list = temp.get("endpoints")
    for i in endpoints_list:
        list_endpoints_path.append(i.get("path"))
        try:
            dict_of_json[i.get("path")] = i.get('method')
        except:
            pass
    return [dict_of_json,list_endpoints_path,prefix_list]

    
def create_app(config):
    app = Flask(__name__)
    temp = create(config)
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>', methods=["GET", "POST", "DELETE", "PUT"])
    def catch_all(path):
        count  = 0
        list_of_tags = path.split("/")
        for i in range(len(temp[2])):
            if i > len(list_of_tags)-1:
                return "Invalid end point"
            elif list_of_tags[i] in temp[2]:
                count = count +1
        if count == len(temp[2]):
            list_of_tags = list_of_tags[count:]
            k = ""
            for i in range(len(list_of_tags)):
                k = k+"/"+ list_of_tags[i]
            if k in temp[1]:
                return str(url_methods(k, request.method,temp[0]))
            else:
                return "Invalid end point"
        else:
            return "invalid end point"
    return app
