from mock_rest import *
import json
from main import convert
class for_objects():
    def __init__(self,temp):
        self.name  =  temp.get("name")
        self.version  =  temp.get("version")
        self.endpoints  =  temp.get("endpoints")
        self.prefix  =  temp.get("prefix")
     
    def get_app_obj(self):
        return MockREST(self.name,self.version,self.prefix,self.endpoints)

  #  def get_endpoint_obj(self):
  #    return self.endpoints
    def get_method_obj(self,path):
        for end_p in self.endpoints:
            if end_p.get("path")==path:
                return EndPoint(path,end_p.get("method"))
    
    def get_result(self,method)
    
file_path = "/home/manojkumar/git/apibox/examples/sample1.json"
json_obj = json.load(open(file_path))
temp = convert(json_obj)
p = for_objects(temp)
print p.get_method_obj("/login")    
