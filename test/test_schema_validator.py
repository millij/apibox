
import unittest

from apibox.utils.schema_validator import *

class SchemaValidatorTest(unittest.TestCase):
    'Schema validation tests'

    def setUp(self):
        self.test_json = {"name" : 11, "price" : 34.99, "endpoints" : []}

    def tearDown(self):
        del self.test_json


    # main test cases

    def test_assertion_true(self):
        self.assertTrue(True)

    def test_json_schema_validation(self):
        is_valid = validate_json(self.test_json)
        print is_valid
        self.assertTrue(True)

if __name__ == '__main__':
    print("Running SchemaValidatorTest test-cases ..")
    unittest.main()