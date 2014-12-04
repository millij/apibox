
from flask import Flask, jsonify,request
from endpoints import enp_path,endpoints_list, dfp
from lambdatest import Operations
k = Operations()
app = Flask(__name__)
@app.route('/',defaults={'path': ''})
@app.route('/<path:path>',methods = ["GET","POST","PUT","DELETE"])
def catch_all(path):
	if request.method == "POST":
		if "/"+path in enp_path:
			existing_data = list(dict(dfp["/"+path]['success']))
			print existing_data
			existing_data.append(request.data)
			dfp["/"+path]['success'] = existing_data
			return str()
		        		
	    	else:
			return "invalid endpoint"

	if "/"+path in enp_path:

		value = [i["result"]["success"] for i in endpoints_list if i["path"] == "/"+path if "GET" in i["methods"]]
		if len(value)==0:
			return "Does not support GET method"
		else:

			return str([	dfp["/"+path]["success"]][:])
	        		
    	else:
		return "invalid endpoint"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


