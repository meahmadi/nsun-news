import sys
from PySide.QtCore import *
from PySide.QtGui import *

import window
import window_resources
 
app = QApplication(sys.argv)

if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Systray",
                "I couldn't detect any system tray on this system.")
        sys.exit(1) 
QApplication.setQuitOnLastWindowClosed(False) 
 
main = window.Window()
main.show()
 
sys.exit(app.exec_())