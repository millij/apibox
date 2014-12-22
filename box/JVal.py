import json
import collections


check_list=[]
def validator(file_name):
	''' validates and return whether the given json file is valid one are not

	input:json file path

	returns True or False .'''
	data=parse(file_name)
	if type(data.get("endpoints"))==list:
   		for end_p in data.get("endpoints"):
			if type(end_p.get("path"))==unicode and type(end_p.get("method"))==list:	
				for methods in end_p.get("method"):
					for method in methods.keys():
						check_list.append(val_met(method,methods.get(method)))
	for check in check_list:
		if check==False:
			return False
	else:
		return  True					
	

def val_met(method,results):
	'''
	validates  whether the methods in the json file are in required format

	input:method type (GET or PUT etc..) and value of the Method.
	'''
	list_results=[]
	for result in results.keys():
		if (method=="PUT" or "GET" or "DELETE") and ("failure" in results.keys()) and ("success" in results.keys()):
				if type(results.get(result))==unicode or list:
					check_list.append(True)	
		elif (method=="POST") and ("failure" in results.keys()) and ("success" in results.keys()) and ("data" in results.keys()):
			if type(result.get(result))==unicode :
					check_list.append(True)	
		else:
			check_list.append(False)	

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

