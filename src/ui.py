# Copyright (c) 2026 OrdoServus
# Licensed under the MIT License

import os
from PyQt5.QtCore import QUrl, Qt, QTimer, QDateTime, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QMessageBox,
                             QSystemTrayIcon, QMenu, QFileDialog, QStyle, QDialog,
                             QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTextEdit, QPushButton)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineDownloadItem, QWebEnginePage
from PyQt5.QtGui import QKeySequence, QIcon, QDesktopServices

try:
    from updater import check_for_updates
    UPDATER_AVAILABLE = True
except ImportError:
    UPDATER_AVAILABLE = False

from settings import AppSettings
from __version__ import __version__

class CustomWebEnginePage(QWebEnginePage):
    external_link_clicked = pyqtSignal(QUrl)
    
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self.allowed_domains = ['sob.ch', 'www.sob.ch']

    def acceptNavigationRequest(self, url, nav_type, isMainFrame):
        if nav_type == QWebEnginePage.NavigationTypeLinkClicked:
            domain = url.host()
            
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if domain == allowed_domain or domain.endswith('.' + allowed_domain):
                    is_allowed = True
                    break
            
            if is_allowed:
                return True
            else:
                # Externe Links in neuem Fenster öffnen
                self.external_link_clicked.emit(url)
                return False 
        
        return True
    
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        if "wasm" in message.lower() and "signature" in message.lower():
            return

class ProfessionalWebApp(QMainWindow):
    def __init__(self, url, app_name="OrdoServus Desktop", github_repo="OrdoServus/Desktop-test", feedback_url=None):
        super().__init__()
        self.home_url = url
        self.app_name = app_name
        self.github_repo = github_repo
        self.feedback_url = feedback_url
        self.settings = AppSettings()

        self.init_ui()
        self.restore_settings()
        self.create_system_tray()

        if UPDATER_AVAILABLE and github_repo:
            QTimer.singleShot(2000, lambda: check_for_updates(self, __version__, github_repo, silent=True))

    def init_ui(self):
        self.setWindowTitle(self.app_name)

        profile = QWebEngineProfile.defaultProfile()
        
        settings = profile.settings()
        settings.setAttribute(settings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(settings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(settings.WebAttribute.WebGLEnabled, True)
        
        self.browser = QWebEngineView()
        self.custom_page = CustomWebEnginePage(profile, self.browser)
        self.browser.setPage(self.custom_page)
        
        # Verbinde externes Link-Signal
        self.custom_page.external_link_clicked.connect(self.open_external_link)
        
        self.setCentralWidget(self.browser)
        self.browser.setUrl(QUrl(self.home_url))
        
        self.browser.setContextMenuPolicy(Qt.NoContextMenu)

        self.create_menu()

    def create_menu(self):
        menubar = self.menuBar()

        # Datei-Menü
        file_menu = menubar.addMenu('&Datei')

        # Neu laden
        reload_action = QAction('&Neu laden', self)
        reload_action.setShortcut(QKeySequence('F5'))
        reload_action.triggered.connect(self.reload_page)
        file_menu.addAction(reload_action)

        file_menu.addSeparator()

        # Beenden
        exit_action = QAction('&Beenden', self)
        exit_action.setShortcut(QKeySequence('Ctrl+Q'))
        exit_action.triggered.connect(self.quit_application)
        file_menu.addAction(exit_action)

        file_menu.addSeparator()

        # Feedback
        if self.feedback_url:
            feedback_action = QAction('&Feedback geben', self)
            feedback_action.triggered.connect(self.open_feedback)
            file_menu.addAction(feedback_action)

        # Navigation-Menü
        nav_menu = menubar.addMenu('&Navigation')

        # Zurück
        back_action = QAction('&Zurück', self)
        back_action.setShortcut(QKeySequence('Alt+Left'))
        back_action.triggered.connect(self.browser.back)
        nav_menu.addAction(back_action)

        # Vorwärts
        forward_action = QAction('&Vorwärts', self)
        forward_action.setShortcut(QKeySequence('Alt+Right'))
        forward_action.triggered.connect(self.browser.forward)
        nav_menu.addAction(forward_action)

        nav_menu.addSeparator()

        # Startseite
        home_action = QAction('&Startseite', self)
        home_action.setShortcut(QKeySequence('Alt+Home'))
        home_action.triggered.connect(self.go_home)
        nav_menu.addAction(home_action)

        # Ansicht-Menü
        view_menu = menubar.addMenu('&Ansicht')

        # Vollbild
        fullscreen_action = QAction('&Vollbild', self)
        fullscreen_action.setShortcut(QKeySequence('F11'))
        fullscreen_action.setCheckable(True)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)

        view_menu.addSeparator()

        # Zoom vergrößern
        zoom_in_action = QAction('Vergrößern', self)
        zoom_in_action.setShortcut(QKeySequence('Ctrl++'))
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)

        # Zoom verkleinern
        zoom_out_action = QAction('Verkleinern', self)
        zoom_out_action.setShortcut(QKeySequence('Ctrl+-'))
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)

        # Zoom zurücksetzen
        zoom_reset_action = QAction('Zoom zurücksetzen', self)
        zoom_reset_action.setShortcut(QKeySequence('Ctrl+0'))
        zoom_reset_action.triggered.connect(self.zoom_reset)
        view_menu.addAction(zoom_reset_action)

        # Hilfe-Menü
        help_menu = menubar.addMenu('&Hilfe')

        # Update prüfen
        if UPDATER_AVAILABLE and self.github_repo:
            update_action = QAction('Nach &Updates suchen', self)
            update_action.triggered.connect(self.check_updates)
            help_menu.addAction(update_action)
            help_menu.addSeparator()

        # Über
        about_action = QAction('&Über', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_system_tray(self):
        self.tray_icon = QSystemTrayIcon(self)

        icon_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icon.ico')
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
        else:
            icon = self.style().standardIcon(QStyle.SP_ComputerIcon)
        self.tray_icon.setIcon(icon)

        tray_menu = QMenu()

        show_action = QAction("Anzeigen", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        hide_action = QAction("Verbergen", self)
        hide_action.triggered.connect(self.hide)
        tray_menu.addAction(hide_action)

        tray_menu.addSeparator()

        quit_action = QAction("Beenden", self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.activateWindow()

    def reload_page(self):
        self.browser.reload()

    def go_home(self):
        self.browser.setUrl(QUrl(self.home_url))

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def zoom_in(self):
        current_zoom = self.browser.zoomFactor()
        new_zoom = current_zoom + 0.1
        self.browser.setZoomFactor(new_zoom)
        self.settings.set_zoom_level(new_zoom)

    def zoom_out(self):
        current_zoom = self.browser.zoomFactor()
        new_zoom = current_zoom - 0.1
        self.browser.setZoomFactor(new_zoom)
        self.settings.set_zoom_level(new_zoom)

    def zoom_reset(self):
        self.browser.setZoomFactor(1.0)
        self.settings.set_zoom_level(1.0)

    def open_feedback(self):
        if self.feedback_url:
            QDesktopServices.openUrl(QUrl(self.feedback_url))
        else:
            QMessageBox.information(
                self,
                "Feedback",
                "Keine Feedback-URL konfiguriert.\n\n"
                "Bitte setze die FEEDBACK_URL Variable in main.py"
            )

    def open_external_link(self, url):
        """Öffnet externe Links in einem neuen Fenster"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Externer Link")
        dialog.setGeometry(100, 100, 1000, 700)
        
        layout = QVBoxLayout()
        dialog.setLayout(layout)
        
        # Info-Label
        info_label = QLabel(f"Externe URL: {url.toString()}")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # WebView für externe Seite
        external_browser = QWebEngineView()
        external_browser.setUrl(url)
        layout.addWidget(external_browser)
        
        # Schließen-Button
        close_btn = QPushButton("Schließen")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec_()

    def show_about(self):
        update_info = ""
        if UPDATER_AVAILABLE and self.github_repo:
            update_info = f"\n\nGitHub: github.com/{self.github_repo}"

        QMessageBox.about(
            self,
            f'Über {self.app_name}',
            f'{self.app_name} v{__version__}\n\n'
            f'{update_info}\n\n'
            'Entwickelt von OrdoServus'
        )

    def check_updates(self):
        if UPDATER_AVAILABLE:
            if self.github_repo:
                check_for_updates(self, __version__, self.github_repo, silent=False)
            else:
                QMessageBox.information(
                    self,
                    "Keine GitHub-Repo konfiguriert",
                    "Es ist keine GitHub-Repository für Updates konfiguriert.\n\n"
                    "Bearbeite die Variable GITHUB_REPO im Code, um Updates zu aktivieren."
                )
        else:
            QMessageBox.information(
                self,
                "Updater nicht verfügbar",
                "Der Updater ist nicht verfügbar. Stelle sicher, dass 'updater.py' vorhanden ist."
            )

    def restore_settings(self):
        self.settings.restore_geometry(self)
        zoom_level = self.settings.get_zoom_level()
        self.browser.setZoomFactor(zoom_level)

    def save_settings(self):
        self.settings.save_geometry(self)
        self.settings.set_zoom_level(self.browser.zoomFactor())

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            self.app_name,
            "Anwendung läuft im Hintergrund weiter",
            QSystemTrayIcon.Information,
            2000
        )

    def quit_application(self):
        self.save_settings()
        self.tray_icon.hide()
        QApplication.quit()
