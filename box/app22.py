from flask import Flask, jsonify, request, render_template, redirect, url_for
import ast
import json
import collections
import os


def convert(data):
    '''
    converts json object to dictionary

    Input:

    - data: json object

    Return: dictionary

    '''
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


def url_methods(path, method):
    '''
    takes path as url and method as one of the  methods and return the appropriate value

    Inputs:

    - path: endpoint path

    - method: enum value ["GET","POST","DELETE","PUT"], here this method is mostly for GET

    Return: appropriate value

    '''
    if method in dfp[path][0]:
        return dfp[path][0][method]["success"]
    else:
        return "This method is not supported"


def check(ori, enp_path):
    for path in enp_path:
        if ori in path:
            return True
    return False

dfp = {}
enp_path = []


def create_app(config):
    app = Flask(__name__)
    file_name = config
    obj = json.load(open(file_name))
    d = convert(obj)
    endpoints_list = d["endpoints"]
    for i in endpoints_list:
        enp_path.append(i["path"])
        try:
            dfp[i["path"]] = i['method']
        except:
            pass

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>', methods=["GET", "POST", "DELETE", "PUT"])
    def catch_all(path):
        k = "/" + path
        if k in enp_path:
            return str(url_methods(k, request.method))
        else:
            return "Invalid end point"
    return app
