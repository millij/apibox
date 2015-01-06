#!flask/bin/python
from flask import Flask, jsonify, make_response, abort, request

app = Flask(__name__)


""" Routes for UI Support """

@app.route("/", methods=["GET"])
@app.route("/app", methods=["GET"])
def apps_home():
    """
    Return all existing apps as JSON
    """
    pass

@app.route("/app/<app_name>", methods=["GET", "POST", "PUT", "DELETE"])
def app_handler(app_name):
    """
    Applications handler
    """
    if request.method == 'GET':
        # GET: Return app details
        print "GET"
    elif request.method == 'POST':
        # POST: Create new App
        print "POST"
    elif request.method == 'PUT':
        # PUT: Update the App
        print "PUT"
    else:
        # DELETE: Delete the APP
        print "DELETE" 

    pass


@app.route("/app/<app_name>/start", methods=["GET"])
def app_handler_start(app_name):
    """
    Starts the app with the given name
    """
    pass

@app.route("/app/<app_name>/stop", methods=["GET"])
def app_handler_stop(app_name):
    """
    Stops the app with the given name
    """
    pass


@app.route("/app/<app_name>/endpoint", methods=["GET", "POST", "PUT", "DELETE"])
def app_endpoint_handler(app_name):
    """
    Applications endpoints handler
    :param app_name: Unique name of the application
    """
    if request.method == 'GET':
        # GET: Returns all app endpoints 
        print "GET"
    elif request.method == 'POST':
        # POST: Create new endpoint for App 
        print "POST"
    elif request.method == 'PUT':
        # PUT: Update the endpoint for App
        print "PUT"
    else:
        # DELETE: Delete the endpoint for App
        print "DELETE" 

    pass



""" Routes / error handling """

@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'error': 'Page Not found'}), 404)

@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'error': str(error)}), 500)


"""
Note: This is for testing Only
TODO remove
"""
if __name__ == '__main__':
    app.run(debug=True)

