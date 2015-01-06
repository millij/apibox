from mock_rest import *
app_container = {}
def launch(host, port, mock_rest):
    """
    Launches a new mock rest server with the passed configuration.
    """
    #mock_rest_obj = MockREST.from_json(mr_json)
    #app_name = host + "_" + port
    #app_container.update({app_name:mock_rest_obj})
    from flask import Flask, request
    app = Flask(__name__)
    @app.route("/login")
    def h():
        print str(mock_rest.endpoints[0])
        path = "/login"
        method = "GET"
        me = mock_rest.get_endpoint(path)
        mee = EndPoint(path,me)
        return str(mee.get_method("GET")) 

    app.run(debug=True,host = host,port = port)

if __name__ == "__main__":
    ep_m = EndPointMethod("GET", "", "hello hi")
    mock_rest = MockREST("mr_test", "", "", None)
    mr_ep1 = EndPoint("/login", [])
           

    mock_rest.add_endPoint(mr_ep1)

    #print str(mr_ep1)
    #print str(mock_rest.endpoints[0])

    launch("0.0.0.0",5000,mock_rest)
