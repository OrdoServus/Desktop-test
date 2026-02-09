# Copyright (c) 2026 OrdoServus
# Licensed under the MIT License

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, application_path)

from ui import ProfessionalWebApp

def main():
    APP_NAME = "OrdoServus Desktop"
    TARGET_URL = "https://test-wiki-phi.vercel.app"
    GITHUB_REPO = "OrdoServus/Desktop-test"

    try:
        import ctypes
        myappid = 'ordoservus.desktop.app.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)

    icon_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icon.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        print(f"Icon loaded successfully from {icon_path}")
    else:
        print(f"Icon not found at {icon_path}")

    window = ProfessionalWebApp(TARGET_URL, APP_NAME, GITHUB_REPO)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
