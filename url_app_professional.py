import sys
import os
import json
from PyQt5.QtCore import QUrl, Qt, QSettings, QSize
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QMessageBox, 
                             QSystemTrayIcon, QMenu, QFileDialog, QStyle)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineDownloadItem
from PyQt5.QtGui import QKeySequence, QIcon

# Updater importieren (wenn vorhanden)
try:
    from updater import check_for_updates
    UPDATER_AVAILABLE = True
except ImportError:
    UPDATER_AVAILABLE = False

# Version der App
APP_VERSION = "0.1"

class ProfessionalWebApp(QMainWindow):
    def __init__(self, url, app_name="OrdoServus APP", github_repo="OrdoServus/Desktop-test"):
        super().__init__()
        self.home_url = url
        self.app_name = app_name
        self.github_repo = github_repo
        self.settings = QSettings("OrdoServus", app_name)
        self.dark_mode = self.settings.value("dark_mode", False, type=bool)
        
        self.init_ui()
        self.restore_settings()
        self.create_system_tray()
        
        if UPDATER_AVAILABLE and github_repo:
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(2000, lambda: check_for_updates(self, APP_VERSION, github_repo, silent=True))
    
    def init_ui(self):
        self.setWindowTitle(self.app_name)
        
        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.on_download_requested)
        
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.browser.setUrl(QUrl(self.home_url))
        
        self.create_menu()
        self.apply_theme()
    
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
        
        nav_menu.addSeparator()
        
        # Ansicht-Menü
        view_menu = menubar.addMenu('&Ansicht')
        
        # Dark Mode
        self.dark_mode_action = QAction('&Dark Mode', self)
        self.dark_mode_action.setCheckable(True)
        self.dark_mode_action.setChecked(self.dark_mode)
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        view_menu.addAction(self.dark_mode_action)
        
        view_menu.addSeparator()
        
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

        if os.path.exists("icon.ico"):
            icon = QIcon("icon.ico")
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
    
    def on_download_requested(self, download):
        path, _ = QFileDialog.getSaveFileName(
            self, 
            "Datei speichern", 
            download.suggestedFileName()
        )
        
        if path:
            download.setPath(path)
            download.accept()
            
            download.finished.connect(lambda: self.download_finished(path))
            download.downloadProgress.connect(self.download_progress)
    
    def download_finished(self, path):
        self.tray_icon.showMessage(
            "Download abgeschlossen",
            f"Datei gespeichert: {os.path.basename(path)}",
            QSystemTrayIcon.Information,
            3000
        )
    
    def download_progress(self, bytes_received, bytes_total):
        if bytes_total > 0:
            progress = int((bytes_received / bytes_total) * 100)
            self.setWindowTitle(f"{self.app_name} - Download: {progress}%")
    
    def reload_page(self):
        self.browser.reload()
    
    def go_home(self):
        self.browser.setUrl(QUrl(self.home_url))
    
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.settings.setValue("dark_mode", self.dark_mode)
        self.apply_theme()
    
    def apply_theme(self):
        if self.dark_mode:
            # Dark Mode
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1e1e1e;
                }
                QMenuBar {
                    background-color: #2d2d2d;
                    color: #ffffff;
                }
                QMenuBar::item:selected {
                    background-color: #3d3d3d;
                }
                QMenu {
                    background-color: #2d2d2d;
                    color: #ffffff;
                }
                QMenu::item:selected {
                    background-color: #3d3d3d;
                }
            """)
        else:
            self.setStyleSheet("")
    
    def zoom_in(self):
        current_zoom = self.browser.zoomFactor()
        new_zoom = current_zoom + 0.1
        self.browser.setZoomFactor(new_zoom)
        self.settings.setValue("zoom_level", new_zoom)
    
    def zoom_out(self):
        current_zoom = self.browser.zoomFactor()
        new_zoom = current_zoom - 0.1
        self.browser.setZoomFactor(new_zoom)
        self.settings.setValue("zoom_level", new_zoom)
    
    def zoom_reset(self):
        self.browser.setZoomFactor(1.0)
        self.settings.setValue("zoom_level", 1.0)
    
    def show_about(self):
        update_info = ""
        if UPDATER_AVAILABLE and self.github_repo:
            update_info = f"\n\nGitHub: github.com/{self.github_repo}"
        
        QMessageBox.about(
            self, 
            f'Über {self.app_name}', 
            f'{self.app_name} v{APP_VERSION}\n\n'
            f'{update_info}\n\n'
            'Entwickelt von OrdoServus'
        )
    
    def check_updates(self):
        if UPDATER_AVAILABLE:
            if self.github_repo:
                check_for_updates(self, APP_VERSION, self.github_repo, silent=False)
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
        if self.settings.value("geometry"):
            self.restoreGeometry(self.settings.value("geometry"))
        else:
            self.setGeometry(100, 100, 1200, 800)
        
        zoom_level = self.settings.value("zoom_level", 1.0, type=float)
        self.browser.setZoomFactor(zoom_level)
    
    def save_settings(self):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("zoom_level", self.browser.zoomFactor())
        self.settings.setValue("dark_mode", self.dark_mode)
    
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

def main():
    APP_NAME = "OrdoServus APP"
    TARGET_URL = "https://www.sob.ch"
    GITHUB_REPO = "OrdoServus/Desktop-test"
    
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    
    app.setWindowIcon(QIcon("icon.ico"))
    
    window = ProfessionalWebApp(TARGET_URL, APP_NAME, GITHUB_REPO)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
