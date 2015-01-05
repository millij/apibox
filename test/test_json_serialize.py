
"""
Reference : 
http://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object

"""

import unittest
import json

class Student(object):
    'Simple Student definition'

    def __init__(self,name,email,contact,skills,ug=None,pg=None):
        self.email=email
        self.contact=contact
        self.name=name
        self.skills=[skills]
        self.edu={"ug":[ug],"pg":[pg]} 

    def p(self):
        return json.dumps(self.__dict__, sort_keys=True, indent=4)


class JSONSerializeTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # some basic tests
    def test_json_dump(self):
        data = [ { 'a':'A', 'b':(2, 4), 'c':3.0 } ]
        print 'DATA:', repr(data)


    # Object to JSON
    
    # JSON to Object
    


    
    
james = Student("James","j@j.com","+1 7789990007","Python","CS", "CS")
print type(james)
print james.p()

#print vars(james)

print json.dumps(james.__dict__, sort_keys=True)

from collections import namedtuple

def _json_object_hook(d): 
    return namedtuple('Student', d.keys())(*d.values())

def json2obj(data): 
    return json.loads(data, object_hook = _json_object_hook)


json_stu = '{"skills": ["Python"], "contact": "+1 7789990007", "email": "j@j.com", "edu": {"ug": ["CS"], "pg": ["CS"]}, "name": "James"}'

x = json2obj(json_stu)

print type(x)
print x.p()



