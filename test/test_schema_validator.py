import unittest

from apibox.utils.schema_validator import *

class SchemaValidatorTest(unittest.TestCase):
    'Schema validation tests'

    def setUp(self):
        print('Setting up SchemaValidatorTest ..')

    def tearDown(self):
        print('Tearing down SchemaValidatorTest ..')


    # main test cases

    def test_json_schema_validation(self):
        self.assertTrue(True)

    def test_schema(self):
        json = {"name" : 11, "price" : 34.99, "endpoints" : []}
        is_valid = validate_json(json)
        print is_valid
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()