import sys, time
from PySide.QtGui import *
from PySide.QtCore import *

import db

from flask import Flask

class WebServer(QThread):
	app = Flask(__name__)
	def __init__(self,window):
		QThread.__init__(self,window)
		self.window = window

		self.db = None

	@app.route("/")
	def hello():
		return "Hello World!"	
	
	def run(self):
		if self.db is None:
			self.db = db.DB()
			self.db.init_dbs()
		
		self.app.run()
		
		