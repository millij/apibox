import json
import collections

class Operations():

	def getValueFromDict(self,dataDict,mapList):
    		return reduce(lambda d, k: d[k], mapList, dataDict)


	def addNewKey(dataDict, mapList, value):
    		if len(mapList)==1:
			dataDict.upadate({mapList[0]:value})
    		else:
			getValueFromDict(dataDict, mapList[:-1]).update({mapList[-1]:value})


	def updateKeyValue(dataDict, mapList,value):
    		if len(mapList)==1:
			dataDict[mapList[0]] = value
    		else:
			getValueFromDict(dataDict,mapList[:-1])[mapList[-1]] = value


	def deleteKey(dataDict,mapList):
    		if len(mapList)==1:
			del dataDict[mapList[0]]
    		else:
			del getValueFromDict(dataDict,mapList[:-1])[mapList[-1]]


	def load_Json(self,file_name):
		obj = json.load(open(file_name))
		return obj


	def write_Json(modified_data):
		with open(file_name,'w') as f:
			json.dump(modofied_data,f,indent = 4)





