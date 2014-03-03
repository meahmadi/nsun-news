from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *

import webserver
import feedcrawl
import db

class Window(QWidget):
	def __init__(self):
		QWidget.__init__(self)

		self.db = db.DB()
		self.db.init_dbs()
		self.db.init_schemas()
		
		feeds = self.db.get_feeds()
		if len(feeds)==0:
			rsss = open('rss.txt')
			site_name = ""
			for rss in rsss:
				if rss.startswith("\t"):
					rss = rss.strip()
					url = rss[rss.find(":")+1:]
					name = site_name+"-"+rss[:rss.find(":")]
					self.db.save_feed(name,url,"")
				else:
					rss = rss.strip()
					site_name = rss[:rss.find(":")]
		
		self.server = webserver.WebServer(self)
		self.server.start()
		
		self.crawler = feedcrawl.Crawler(self)
		self.crawler.start()
			
		self.icon = QIcon(':/images/icon.png')
	
		self.setLayout(QVBoxLayout())
	
		self.web = QWebView()
		self.web.load(QUrl("http://localhost:5000/"))
		self.layout().addWidget(self.web)
		
		self.setWindowTitle(u"Smart News Reader Just For You")
		self.setWindowFlags(Qt.Tool) 
		self.resize(600, 400)
		
		self.createActions()
		self.createTrayIcon()

	def createActions(self):
		self.minimizeAction = QAction("Mi&nimize", self,
				triggered=self.hide)
 
		self.maximizeAction = QAction("Ma&ximize", self,
				triggered=self.showMaximized)
 
		self.restoreAction = QAction("&Restore", self,
				triggered=self.showNormal)
 
		self.quitAction = QAction("&Quit", self,
				triggered=QApplication.quit)
		
	def createTrayIcon(self):
		self.trayIconMenu = QMenu(self)
		self.trayIconMenu.addAction(self.minimizeAction)
		self.trayIconMenu.addAction(self.maximizeAction)
		self.trayIconMenu.addAction(self.restoreAction)
		self.trayIconMenu.addSeparator()
		self.trayIconMenu.addAction(self.quitAction)
 
		self.trayIcon = QSystemTrayIcon(self)
		self.trayIcon.setContextMenu(self.trayIconMenu)		
		self.trayIcon.messageClicked.connect(self.messageClicked)
		self.trayIcon.activated.connect(self.iconActivated)

		self.trayIcon.setIcon(self.icon)
		self.setWindowIcon(self.icon)
		self.trayIcon.setToolTip(self.windowTitle())
				
		self.trayIcon.show()
		
	def closeEvent(self, event):
		if self.trayIcon.isVisible():
			#QMessageBox.information(self, "Systray",
			#		"The program will keep running in the system tray. To "
			#		"terminate the program, choose <b>Quit</b> in the "
			#		"context menu of the system tray entry.")
			self.hide()
			event.ignore()	
	def iconActivated(self, reason):
		if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
			self.showNormal()
		elif reason == QSystemTrayIcon.MiddleClick:
			self.showMessage()
 
	def showMessage(self):
		self.trayIcon.showMessage("","", self.icon,2000)
 
	def messageClicked(self):
		pass

