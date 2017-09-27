#!/usr/bin/python3

import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from urllib.parse import parse_qs
from cgi import parse_header, parse_multipart
import visiting_city_data as city_table

hostName = ""
hostPort = 8000

class MyServer(BaseHTTPRequestHandler):

	#	GET is for clients geting the predi
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

		self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))

	def parse_POST(self):
		ctype, pdict = parse_header(self.headers['content-type'])
		pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
		print(ctype)
		# import pdb; pdb.set_trace()
		if ctype == 'multipart/form-data':
			postvars = parse_multipart(self.rfile, pdict)
		elif ctype == 'application/x-www-form-urlencoded':
			length = int(self.headers['content-length'])
			postvars = parse_qs(
			self.rfile.read(length),
			keep_blank_values=1)
		else:
			postvars = {}
		return postvars


	#	POST is for submitting data.
	def do_POST(self):
		print( "incomming http: ", self.path )

		self.send_response(200)
		param = self.parse_POST()

		# self.wfile.write(bytes("<p>Thanks</p>", "utf-8"))

		spreadsheetId = '1eqS-m4EPRM4U8Py269jwqUWZGQrKHFkfirATVwD9wAQ'
		result = city_table.insert_city(spreadsheetId, param['longitude'][0].decode(), param['latitude'][0].decode())

		self.send_header('Content-type', 'text/html')
		self.end_headers()

		if result:
			print('Saved')
			self.wfile.write(bytes("Saved!", "utf-8"))
		else:
			print('Not saved')
			self.wfile.write(bytes("Previously saved!", "utf-8"))

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
