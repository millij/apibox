from lambdatest import Operations
from unicode1 import convert
file_name = "ocr.json"
k = Operations()
jsonObj = k.load_Json(file_name)
dictData = convert(jsonObj)
endpoints_list = dictData["endpoints"]
enp_path = []
dfp = {}
for i in endpoints_list:
	enp_path.append(i["path"])
	try:
		dfp[i["path"]]=i['result']
	except: pass
	

