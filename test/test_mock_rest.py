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

    def test_EndPointMethod_init(self):
        # test creation
        ep_mthd = EndPointMethod(self.method_get, self.inp_data_login, self.result_login)

        self.assertIsNotNone(ep_mthd)
        self.assertEqual(ep_mthd.method, "GET")

    def test_EndPointMethod_is_inp_valid(self):
        pass



    # --- EndPoint --- #

    def test_EndPoint_init(self):
        path = "/test_ep_1"
        ep = EndPoint(path, None)

        self.assertEqual(ep.path, path)

        # check the methods
        self.assertIsNotNone(ep.methods)
        self.assertEqual(len(ep.methods), 0)

    def test_EndPoint_init_empty_path(self):
        with self.assertRaises(ValueError):
            ep = EndPoint("", None)

    def test_EndPoint_add_method_typecheck(self):
        ep = EndPoint("ep_add_test", None)

        # add method type check
        with self.assertRaises(TypeError):
            ep.add_method("")

    def test_EndPoint_add_method(self):
        ep = EndPoint("ep_add_test", None)
        ep_method1 = EndPointMethod("GET", {}, {})

        # add method
        ep.add_method(ep_method1)
        self.assertEqual(len(ep.methods), 1)
        self.assertEqual(ep.methods[0].method, "GET")

    def test_EndPoint_remove_method_typecheck(self):
        ep = EndPoint("ep_remove_test", None)

        # remove method type check
        with self.assertRaises(TypeError):
            ep.remove_method("")

    def test_EndPoint_remove_method_safe_missing_value(self):
        ep = EndPoint("ep_remove_test", None)

        # remove with no ValueError
        ep.remove_method(EndPointMethod("GET", {}, {}))
        self.assertEqual(len(ep.methods), 0)

    def test_EndPoint_remove_method(self):
        ep = EndPoint("ep_remove_test", None)
        ep_method1 = EndPointMethod("GET", {}, {})
        ep_method2 = EndPointMethod("POST", {}, {})

        ep.add_method(ep_method1)
        ep.add_method(ep_method2)
        self.assertEqual(len(ep.methods), 2)
        self.assertEqual(ep.methods[0].method, "GET")

        # remove method 
        ep.remove_method(ep_method1)
        self.assertEqual(len(ep.methods), 1)
        self.assertEqual(ep.methods[0].method, "POST")





    # --- MockREST --- #

    def test_MockREST_init(self):
        name = "test_mock_rest"
        version = "v1"
        prefix = "/api/v1"
        mr = MockREST(name, version, prefix, None)

        self.assertEqual(mr.name, name)
        self.assertEqual(mr.version, version)
        self.assertEqual(mr.prefix, prefix)

        # check the endpoints
        self.assertIsNotNone(mr.endpoints)
        self.assertEqual(len(mr.endpoints), 0)

    def test_MockREST_init_empty_name(self):
        with self.assertRaises(ValueError):
            mr = MockREST("", "", "", None)

    def test_MockREST_add_endPoint_typecheck(self):
        mr = MockREST("mr_add_ep_test", "", "", None)

        # add method type check
        with self.assertRaises(TypeError):
            mr.add_endPoint("")

    def test_MockREST_add_endPoint(self):
        mr = MockREST("mr_add_ep_test", "", "", None)

        mr_ep1_path = "/ep1_path"
        mr_ep1 = EndPoint(mr_ep1_path, None)

        # add method
        mr.add_endPoint(mr_ep1)
        self.assertEqual(len(mr.endpoints), 1)
        self.assertEqual(mr.endpoints[0].path, mr_ep1_path)

    def test_MockREST_remove_endPoint_typecheck(self):
        mr = MockREST("mr_remove_ep_test", "", "", None)

        # remove method type check
        with self.assertRaises(TypeError):
            mr.remove_endPoint("")

    def test_MockREST_remove_endPoint_safe_missing_value(self):
        mr = MockREST("mr_remove_ep_test", "", "", None)

        # remove with no ValueError
        mr.remove_endPoint(EndPoint("/some_path", None))
        self.assertEqual(len(mr.endpoints), 0)

    def test_MockREST_remove_endPoint(self):
        mr = MockREST("mr_remove_ep_test", "", "", None)

        mr_ep1_path = "/ep1_path"
        mr_ep1 = EndPoint(mr_ep1_path, None)
        mr_ep2_path = "/ep2_path"
        mr_ep2 = EndPoint(mr_ep2_path, None)

        mr.add_endPoint(mr_ep1)
        mr.add_endPoint(mr_ep2)
        self.assertEqual(len(mr.endpoints), 2)
        self.assertEqual(mr.endpoints[0].path, mr_ep1_path)

        # remove method 
        mr.remove_endPoint(mr_ep1)
        self.assertEqual(len(mr.endpoints), 1)
        self.assertEqual(mr.endpoints[0].path, mr_ep2_path)



    # --- MockRESTBase Related --- #

    def test_MockRESTBase_eq_(self):
        # EndPointMethod
        epm1 = EndPointMethod("GET", {}, {})
        epm2 = EndPointMethod("GET", {}, {})
        self.assertEqual(epm1, epm2)

        # EndPoint
        ep1 = EndPoint("/path", None)
        ep2 = EndPoint("/path", None)
        self.assertEqual(ep1, ep2)

        ep1.add_method(epm1)
        self.assertNotEqual(ep1, ep2)
        ep2.add_method(epm2)
        self.assertEqual(ep1, ep2)


    # TODO add tests for other


if __name__ == '__main__':
    print("Running MockRESTTest test-cases ..")
    unittest.main()
