import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import time
import os
import random
from tornado import gen
import socket
import glob

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)

clients = dict()
current_gif = None
static_path = os.path.join(os.path.dirname(__file__), "static")
gifs_pattern = os.path.join(static_path, "gifs/*.gif")


class IndexHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		kwargs = {'ws_host' : socket.gethostname()}
		self.render('index.html', **kwargs)


# class ShowGifHandler(tornado.web.RequestHandler):

# 	@tornado.web.asynchronous
# 	def get(self):
# 		global clients

# 		url = self.get_argument("url")
# 		broadcast_gif( url )

# 		self.write("OK "+url)
# 		self.finish()


class WebSocketHandler(tornado.websocket.WebSocketHandler):
	
	def check_origin(self, origin):
		return True

	def open(self, *args):
		global clients, current_gif 

		self.id = self.get_argument("Id")
		self.stream.set_nodelay(True)
		clients[self.id] = {"id": self.id, "object": self}

		msg = json.dumps({'action': 'showgif', 'url': current_gif});
		self.write_message(msg)

	def on_message(self, message):        
		"""
		when we receive some message we want some message handler..
		for this example i will just print message to console
		"""
		print "Client %s received a message : %s" % (self.id, message)
		
	def on_close(self):
		global clients

		if self.id in clients:
			del clients[self.id]


app = tornado.web.Application([
	(r'/', IndexHandler),
	#(r'/gif', ShowGifHandler),
	(r'/ws', WebSocketHandler),
	(r'/static/(.*)', tornado.web.StaticFileHandler, { 'path': static_path }),
])

@gen.engine
def loop():
	global clients, current_gif 

	#current_gif = "/static/gifs/" + random.choice(os.listdir(gifs_folder))
	gifs = glob.glob( gifs_pattern )
	filename = random.choice( gifs )
	this_dir = os.path.dirname(__file__)
	current_gif = filename.replace(this_dir, "")
	
	msg = json.dumps({'action': 'showgif', 'url': current_gif});
	for id, client in clients.iteritems():
		client['object'].write_message(msg)

	yield gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 10)
	tornado.ioloop.IOLoop.instance().add_callback(loop)



if __name__ == '__main__':
	parse_command_line()
	app.listen(options.port)
	loop()
	tornado.ioloop.IOLoop.instance().start()
   

