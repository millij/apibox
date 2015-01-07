import json
import os
import logging as log
from jsonschema import validate

JSON_SCHEMA_REL_PATH = "/apibox/utils/schema.json"


def get_abs_path(rel_path):
    """
    Takes a relative path as input and returns the absolute path of the same.
    """
    cwd = os.getcwd()
    abs_path = cwd + rel_path

    log.debug("absolute path : %s", abs_path)
    return abs_path


def is_json_valid(in_json):
    """
    validates whether the json file is in required schema or not.

    :param in_json: json to be validated
    :returns: boolean
    """
    # load schema
    schema_path = get_abs_path(JSON_SCHEMA_REL_PATH)
    schema_data = open(schema_path, "r+")
    schema = json.load(schema_data)

    log.debug("In coming JSON for validation : %s", str(in_json))

    # validate the incoming json
    if validate(in_json, schema) == None :
        return True
    else:
        return False


def validate_file_content(file_path, file_type):
    """
    Validates the file contents
    """
    if file_type == "JSON":
        # read file for json content
        json_content = json.load(open(file_path))

        # validate and return
        if is_json_valid(json_content):
            return True, json_content
        else:
            return False, None

    else:
        raise ValueError("Unkown file tyre")








