from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from box import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(8000, address='0.0.0.0')
print "running at port 8000 and address ip" +str(http_server)
IOLoop.instance().start()