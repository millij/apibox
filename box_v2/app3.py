from flask import Flask, jsonify,request, render_template
import ast
import json
import collections


app = Flask(__name__)

'''
converts json object to dictionary

Input:

- data: json onject

Return:

'''
def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


'''
takes path as url and method as one of the  methods and return the appropriate value

Inputs: 

- path: endpoint path

- method: enum value ["GET","POST","DELETE","PUT"]

'''
def url_methods(path,method):
    if method in dfp[path][0]:
        return dfp[path][0][method]["success"]
    else:
        return "This method is not supported"


file_name = "ocr.json" 
obj = json.load(open(file_name)) 
d = convert(obj)
endpoints_list = d["endpoints"]
enp_path = []
dfp = {}
methods = {}
for i in endpoints_list:
	enp_path.append(i["path"])
	try:
		dfp[i["path"]]=i['method']
	except: pass

'''
takes path as url and method as one of the  methods and return the appropriate value

Inputs: 

- path: endpoint path

- method: enum value ["GET","POST","DELETE","PUT"]

'''
def url_methods(path,method):
    if method in dfp[path][0]:
        return str(dfp[path][0][method]["success"])
    else:
        return "This method is not supported"



'''
This method is mainly for post method

compares data field and key to be added

Input:

- data: data field in post method

- dict2: key value to be added

Output:

- TRue or False

'''


def compare_dictionaries(data,dict2):
    keys_of_data = data.keys()
    keys2 = dict2.keys()
    if len(keys_of_data)==len(keys2):
        count = 0
        for i in range(len(keys_of_data)):
            if len(data[keys_of_data[i]].keys()) == len(dict2[keys2[i]].keys()):
                count = count +1
        if count == len(keys_of_data):
            return True
        else:
            return False
    else:
        return False


'''

Adds new key value 

Input:

- key: key value to be added

- path: respective path in which key value to be added

'''

def post_method(key,path):
    try:
        key = ast.literal_eval(key)
        print key
        data = dfp[path][0]["POST"]["data"]
        if compare_dictionaries(data,key):
            existing_data = dfp[path][0]["GET"]["success"]
            existing_data.append(key)
            dfp[path][0]["GET"]["success"] = existing_data
            return str(dfp[path][0]["POST"]["success"])
        else:
            return "Invalid Key pair" +str(request.data)
    except:
        return "invalid Key Value Pair"


'''

Modifies key value 

Input:

- key: key value to be modified

- path: respective path in which key value to be modified

'''

def put_method(key,path):
    try:
        key =  ast.literal_eval(key)
        keys = key.keys()
        list_success = dfp[path][0]["GET"]["success"]        
        for i in range(len(list_success)):
            if keys[0] in list_success[i]:
                list_success[i][keys[0]] = key[keys[0]]
                dfp[path][0]["GET"]["success"] = list_success
                return str(dfp[path][0]["PUT"]["success"])
            else:
                return "The key you want to modifty does not exit"
    except:
        return "Invalid Key Value Pair"

'''

Deletes key value 

Input:

- key: key value to be deleted

- path: respective path in which key value to be deleted

'''


def delete_method(key,path):
    try:
        key =  ast.literal_eval(key)
        keys = key.keys()
        list_success = dfp[path][0]["GET"]["success"]  
        for i in range(len(list_success)):
            print "in for of delete method"
            if keys[0] in list_success[i]:
                del list_success[i][keys[0]]
                dfp[path][0]["GET"]["success"] = list_success
                return str(dfp[path][0]["DELETE"]["success"])
            else:
                return "The key you want to delete does not exit"
    except:
        return "invalid key value pair"


'''

This is the method which takes the Request and Responces accordingly
 
'''
@app.route('/',defaults={'path': ''})
@app.route('/<path:path>',methods = ["GET","POST","DELETE","PUT"])
def catch_all(path):
    k = "/" + path
    if k in enp_path:
        if request.method == "POST":
            return post_method(request.data,k)
        if request.method =="PUT": 
            return put_method(request.data,k)
        if request.method =="DELETE":
            return delete_method(request.data,k)
        if request.method == "GET":
            return url_methods(k,request.method)
            
    else:
        return "Invalid end point"
    
        		
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


