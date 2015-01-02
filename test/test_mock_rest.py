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

    def test_endPoint_create(self):
        path = "/test_ep_1"
        ep = Endpoint(path, None)

        self.assertEqual(ep.path, path)

        # check the methods
        self.assertIsNotNone(ep.methods)
        self.assertEqual(len(ep.methods), 0)

    def test_endPoint_create_empty_path(self):
        with self.assertRaises(ValueError):
            ep = Endpoint("", None)

    def test_endPoint_add_method(self):
        ep = Endpoint("ep_add_test", None)

        # EndPoint methods
        ep_method1 = EndPointMethod()

        with self.assertRaises(TypeError):
            ep.add_method("")

        


    def test_endPoint_method_method(self):
        pass

    # --- MockREST --- #



if __name__ == '__main__':
    print("Running MockRESTTest test-cases ..")
    unittest.main()
