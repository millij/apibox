
import unittest

from apibox.utils.schema_validator import *

class SchemaValidatorTest(unittest.TestCase):
    'Schema validation tests'

    def setUp(self):
        self.test_json_path = "test/test_schema.json"
        self.json_wrong_name = {"name" : "minimal_cms", "endpoints" : []}

    def tearDown(self):
        del self.json_wrong_name


    # main test cases

    def test_is_json_valid_wrong_name(self):
        is_valid = is_json_valid(self.json_wrong_name)


    def test_is_json_valid_correct_schema(self):
        test_json = json.load(open(self.test_json_path))
        is_valid = is_json_valid(self.json_wrong_name)
        self.assertTrue(is_valid)

if __name__ == '__main__':
    print("Running SchemaValidatorTest test-cases ..")
    unittest.main()