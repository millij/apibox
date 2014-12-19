import json
import collections


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


def validator(ob):
	''' validates and return whether the given json file is valid one are not

	input:json file path

	returns json file if valid, else error message .'''
	data=parse(ob)
	con=convert(data)
	if type(con.get("endpoints"))==list:
   		for end_p in con.get("endpoints"):
			if type(end_p.get("path"))==str and type(end_p.get("method"))==list:	
				for method in end_p.get("method"):
					for key in method:
						print type(method.get(key))
						print key
						print ".................."
						if val_met(key,method.get(key)):
							return con
	else:
		return "not valid format" 					
	

def val_met(method,results):
	'''
	validates  whether the methods in the json file are in required format

	input:method type (GET or PUT etc..) and value of the Method.
	'''
	for result in results.keys():
		print result
		if method=="PUT" or "GET" or "DELETE" and result=="success" or "failure":
				if type(results.get(result))==str:
					return True	
		elif method=="POST"and result=="success" or "failure":
			if type(result.get("success"))==str :
					return True
		else:
			return False

'''
def key_type(key):
	if key=="name":
		return str
        if key=="api":
		return dict
	if key=="endpionts":
		return list
	if key=="path":
		return str
	if key=="method":
		return list
	else :
		return "invalid"
'''		

def parse(text):
	'''validates given file is json or not

	input:json file

	return :if valid json, else error message .'''
	try:
		with open(text) as json_file:
       	 		return json.load(json_file)
	except ValueError as e:
        	print('invalid json: %s' % e)
        	return None 

print validator("ocr.json")

#validate({"name":"def"},schema)

