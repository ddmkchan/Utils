import tornado.ioloop
import tornado.httpserver
import tornado.web
import json
from routes import *

if __name__ == "__main__":
    #application.listen(8888)
    http_server = tornado.httpserver.HTTPServer(application)  
    http_server.listen(8888) 
    print "listen to port 8888..."
    tornado.ioloop.IOLoop.instance().start()
