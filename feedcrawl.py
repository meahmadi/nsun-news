import sys, time
from PySide.QtGui import *
from PySide.QtCore import *

import feedparser
import db

class Crawler(QThread):
	
	def __init__(self,window):
		QThread.__init__(self,window)
		self.window = window
		self.db = None
		
	def run(self):
		if self.db is None:
			self.db = db.DB()
			self.db.init_dbs()

		while True:
			feeds = self.db.get_feeds()
			for feed in feeds:
				d = feedparser.parse(feed[2])
				fetchid = self.db.save_fetch(feed[0],d.feed)
				for entry in d.entries:
					self.db.save_news(fetchid,entry)
			
			time.sleep(60*10)
		