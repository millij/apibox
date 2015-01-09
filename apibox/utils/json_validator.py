import json
import collections


check_list = []


def validate(file_name):
    '''
validates and return whether the given json file is valid one are not
input:json file path
returns True or False or error message.
'''

    data = get_json(file_name)
    if not isinstance(data.get("endpoints"), list):
        return "endpoints are not of type list"

    for end_p in data.get("endpoints"):
        if not isinstance(
                end_p.get("path"),
                unicode) and not isinstance(
                end_p.get("method"),
                list):
            return "either method is not of type list or path is not of type string"

        for methods in end_p.get("method"):
            for method in methods.keys():
                check_list.append(validate_method(method, methods.get(method)))

    for check in check_list:
        if not check:
            return False
        else:
            return True


def validate_method(method, results):
    '''
    validates  whether the methods in the json file are in required format
    input:method type (GET or PUT etc..) and value of the Method.
    '''
    if (method == "PUT" or "GET" or "DELETE") and (
            "failure" in results.keys()) and ("success" in results.keys()):
        if isinstance(
                results.get("success"),
                unicode) or list and isinstance(
                results.get("failure"),
                unicode):
            check_list.append(True)
        elif (method == "POST") and ("failure" in results.keys()) and ("success" in results.keys()) and ("data" in results.keys()):
            if isinstance(
                results.get("success"),
                unicode) and isinstance(
                results.get("failure"),
                unicode) and isinstance(
                results.get("data"),
                    dict):
                check_list.append(True)
        else:
            check_list.append(False)


def get_json(file_name):
    '''validates given file is json or not

    input:json file

    return :if valid json, else error message .'''
    try:
        with open(file_name) as json_file:
            return json.load(json_file)
    except ValueError as e:
        print('invalid json: %s' % e)
        return None
