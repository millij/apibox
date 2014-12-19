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

check_list=[]
def validator(file_name):
	''' validates and return whether the given json file is valid one are not

	input:json file path

	returns json file if valid, else error message .'''
	data=parse(file_name)
	if type(data.get("endpoints"))==list:
		print len(data.get("endpoints"))
		#print data.get("endpoints")
   		for end_p in data.get("endpoints"):
			print end_p
			if type(end_p.get("path"))==unicode and type(end_p.get("method"))==list:	
				for methods in end_p.get("method"):
					print "+++++++++++++++++" ,methods
					print "#######################"
					for method in methods.keys():
						print method
						print ".................."
						check_list.append(val_met(method,methods.get(method)))
	for check in check_list:
		if check==False:
			print check
			return "not valid format"
	else:
		return  data					
	

def val_met(method,results):
	'''
	validates  whether the methods in the json file are in required format

	input:method type (GET or PUT etc..) and value of the Method.
	'''
	list_results=[]
	for result in results.keys():
		print results.keys()
		if method=="PUT" or "GET" or "DELETE" and result=="success" or "failure":
				if type(results.get(result))==unicode or list:
					print results.get(result),"**************************"
					check_list.append(True)	
		elif method=="POST"and result=="success" or "failure" or "data":
			if type(result.get(result))==unicode :
					print results.get(result),"**************************"
					check_list.append(True)	
		else:
			check_list.append(False)	

'''
def value_type(key):
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

