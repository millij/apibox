import sys
from flask import Flask, request
# cache = Cache(config={'CACHE_TYPE': 'simple'})

from flask import Flask, jsonify, make_response, abort, request
from multiprocessing import Process

name = sys.argv[1]
port = sys.argv[2]
file_oath= sys.argv[3]

print name, port
app = Flask(name.replace(" ",''))
# cache.init_app(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=["GET", "POST", "DELETE", "PUT"])
def catch_all(path):
    path = "/"+path
    return str(path)



app.run(debug=False, port=int(port))