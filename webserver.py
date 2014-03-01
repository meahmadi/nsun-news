import sys, time
from PySide.QtGui import *
from PySide.QtCore import *

from flask import Flask

class WebServer(QThread):
	app = Flask(__name__)
	def __init__(self,window):
		QThread.__init__(self,window)
		self.window = window

	@app.route("/")
	def hello():
		return "Hello World!"	
	
	def run(self):
		self.app.run()
		
		