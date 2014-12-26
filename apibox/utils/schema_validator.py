import json
import os
from jsonschema import validate 

JSON_SCHEMA_REL_PATH = "/apibox/utils/schema.json"


def get_abs_path(rel_path):
    """
    Takes a relative path as input and returns the absolute path of the same.
    """
    cwd = os.getcwd()
    abs_path = cwd + rel_path

    print "absolute path : " + abs_path
    return abs_path


def validate_json(in_json):
    """
    validates whether the json file is in required schema or not.

    input: json to be validated
    returns: boolean
    """
    # load schema
    schema_path = get_abs_path(JSON_SCHEMA_REL_PATH)
    schema_data = open(schema_path, "r+")
    schema = json.load(schema_data)

    print "------------- Schema ------------"
    print schema

    print "------------- In JSON -----------"
    print in_json

    # validate the incoming json
    if validate(in_json, schema) == None :
        return True
    else:
        return False













