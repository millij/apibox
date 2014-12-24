import json
from jsonschema import validate 


def schema_validate(json_file):
	'''
	validates whether the json file is in required schema or not.

	input:file path

	returns:boolean
	'''
	data=json.load(open(json_file))
	schema=json.load(open("schema.json"))
	if validate(data,schema)==None:
		return True
	else:
		return False
	












