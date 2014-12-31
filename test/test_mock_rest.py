import unittest

from apibox.mock_rest import *

class MockRESTTest(unittest.TestCase):
    'Mock REST related test cases'

    def setUp(self):
        self.method_get = "GET"
        self.inp_data_login = { "username" : "user1", "password" : "passw0rd" }
        self.result_login = { "msg" : "Welcome", "res" : "22dtsadiite34h6##5is" }

    def tearDown(self):
        del self.method_get
        del self.inp_data_login
        del self.result_login


    # --- EndPointMethod --- #

    def test_endPointMethod_create(self):
        # test creation
        ep_mthd = EndPointMethod(self.method_get, self.inp_data_login, self.result_login)

        self.assertIsNotNone(ep_mthd)
        self.assertEqual(ep_mthd.method, "GET")

    def test_endPointMethod_is_inp_valid(self):
        pass


    # --- EndPoint --- #

    def test_endPoint(self):
        pass


    # --- MockREST --- #



if __name__ == '__main__':
    print("Running MockRESTTest test-cases ..")
    unittest.main()