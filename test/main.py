import unittest
import logging
from JVal import validator
from main import url_methods, create

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Stated Running Test case ...')

file_name = "ocr.json"

class TestCases(unittest.TestCase):

    def test_JSON_validator(self):
        logger.info('Running Test case for JSON validator ...')
        self.assertEquals(validator(file_name), True)

    def test_GET_Method(self):
        logger.info('Running Test case for GET Method ...')
        temp = create(file_name)
        k = [{"1":{"u":"XXXX", "p":"****", "x":"11111"}}]
        self.assertEquals(url_methods("/benchmark", "GET", temp[0]), k)

    def test_POST_Method(self):
        logger.info('Running Test case for POST Method ...')
        temp = create(file_name)
        k = "succesfully added new key value"
        self.assertEquals(url_methods("/benchmark", "POST", temp[0]), k)

    def test_PUT_Method(self):
        logger.info('Running Test case for PUT Method ...')
        temp = create(file_name)
        k = "succesfully modified key value"
        self.assertEquals(url_methods("/benchmark", "PUT", temp[0]), k)

    def test_DELETE_Method(self):
        logger.info('Running Test case for DELETE Method ...')
        temp = create(file_name)
        k = "succesfully deleted key value"
        self.assertEquals(url_methods("/benchmark", "DELETE", temp[0]), k)

if __name__ == '__main__':
    unittest.main()

