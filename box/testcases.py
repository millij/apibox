import unittest
from main import url_methods,create
file_name = "ocr.json"
class TestCases(unittest.TestCase):

    def test_GET_Method(self):
        temp = create(file_name)
        k = [{"1":{"u":"XXXX","p":"****","x":"11111"}}]
        self.assertEquals(url_methods("/benchmark","GET",temp[0]),k)

    def test_POST_Method(self):
        temp = create(file_name)
        k = "succesfully added new key value"
        self.assertEquals(url_methods("/benchmark","POST",temp[0]),k)

    def test_PUT_Method(self):
        temp = create(file_name)
        k = "succesfully modified key value"
        self.assertEquals(url_methods("/benchmark","PUT",temp[0]),k)

    def test_DELETE_Method(self):
        temp = create(file_name)
        k = "succesfully deleted key value"
        self.assertEquals(url_methods("/benchmark","DELETE",temp[0]),k)

if __name__ == '__main__':
    unittest.main()

