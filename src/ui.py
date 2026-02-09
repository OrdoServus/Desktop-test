# Copyright (c) 2026 OrdoServus
# Licensed under the MIT License

import os
from PyQt5.QtCore import QUrl, Qt, QTimer, QDateTime
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
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self.allowed_domains = ['sob.ch', 'www.test-wiki-phi.vercel.app']

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
                QDesktopServices.openUrl(url)
                return False
        
        return True

class ProfessionalWebApp(QMainWindow):
    def __init__(self, url, app_name="OrdoServus Desktop", github_repo="OrdoServus/Desktop-test"):
        super().__init__()
        self.home_url = url
        self.app_name = app_name
        self.github_repo = github_repo
        self.settings = AppSettings()
        self.dark_mode = self.settings.get_dark_mode()

        self.init_ui()
        self.restore_settings()
        self.create_system_tray()

        if UPDATER_AVAILABLE and github_repo:
            QTimer.singleShot(2000, lambda: check_for_updates(self, __version__, github_repo, silent=True))

    def init_ui(self):
        self.setWindowTitle(self.app_name)

        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.on_download_requested)

        self.browser = QWebEngineView()
        self.custom_page = CustomWebEnginePage(profile, self.browser)
        self.browser.setPage(self.custom_page)
        
        self.setCentralWidget(self.browser)
        self.browser.setUrl(QUrl(self.home_url))
        
        self.browser.setContextMenuPolicy(Qt.NoContextMenu)

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

        file_menu.addSeparator()

        # Feedback
        feedback_action = QAction('&Feedback', self)
        feedback_action.triggered.connect(self.show_feedback_dialog)
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

    def on_download_requested(self, download):
        try:
            suggested_name = download.suggestedFileName()
            
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            default_path = os.path.join(downloads_path, suggested_name)
            
            path, _ = QFileDialog.getSaveFileName(
                self,
                "Datei speichern",
                default_path,
                "Alle Dateien (*.*)"
            )

            if path:
                download.setPath(path)
                download.accept()
                
                download.finished.connect(lambda: self.download_finished(download, path))
                download.stateChanged.connect(lambda state: self.download_state_changed(download, state))
                
                print(f"Download gestartet: {suggested_name} -> {path}")
            else:
                download.cancel()
                print("Download abgebrochen")
                
        except Exception as e:
            print(f"Fehler beim Download: {e}")
            QMessageBox.warning(
                self,
                "Download-Fehler",
                f"Der Download konnte nicht gestartet werden:\n{str(e)}"
            )

    def download_finished(self, download, path):
        """Called when download is finished"""
        if download.state() == QWebEngineDownloadItem.DownloadCompleted:
            self.tray_icon.showMessage(
                "Download abgeschlossen",
                f"Datei gespeichert: {os.path.basename(path)}",
                QSystemTrayIcon.Information,
                3000
            )
            print(f"Download abgeschlossen: {path}")
        elif download.state() == QWebEngineDownloadItem.DownloadCancelled:
            print(f"Download abgebrochen: {path}")
        elif download.state() == QWebEngineDownloadItem.DownloadInterrupted:
            QMessageBox.warning(
                self,
                "Download unterbrochen",
                f"Der Download wurde unterbrochen:\n{os.path.basename(path)}"
            )
            print(f"Download unterbrochen: {path}")

    def download_state_changed(self, download, state):
        """Track download state changes"""
        if state == QWebEngineDownloadItem.DownloadInProgress:
            received = download.receivedBytes()
            total = download.totalBytes()
            if total > 0:
                progress = int((received / total) * 100)
                self.setWindowTitle(f"{self.app_name} - Download: {progress}%")
        elif state == QWebEngineDownloadItem.DownloadCompleted:
            self.setWindowTitle(self.app_name)

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
        self.settings.set_dark_mode(self.dark_mode)
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
        self.settings.set_zoom_level(new_zoom)

    def zoom_out(self):
        current_zoom = self.browser.zoomFactor()
        new_zoom = current_zoom - 0.1
        self.browser.setZoomFactor(new_zoom)
        self.settings.set_zoom_level(new_zoom)

    def zoom_reset(self):
        self.browser.setZoomFactor(1.0)
        self.settings.set_zoom_level(1.0)

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
        self.settings.set_dark_mode(self.dark_mode)

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

    def show_feedback_dialog(self):
        dialog = FeedbackDialog(self)
        dialog.exec_()


class FeedbackDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Feedback geben")
        self.setModal(True)
        self.resize(400, 300)

        layout = QVBoxLayout()

        # Rating
        rating_layout = QHBoxLayout()
        rating_layout.addWidget(QLabel("Bewertung:"))
        self.rating_combo = QComboBox()
        self.rating_combo.addItems(["1 Stern", "2 Sterne", "3 Sterne", "4 Sterne", "5 Sterne"])
        rating_layout.addWidget(self.rating_combo)
        layout.addLayout(rating_layout)

        # Comments
        layout.addWidget(QLabel("Kommentare:"))
        self.comment_edit = QTextEdit()
        layout.addWidget(self.comment_edit)

        # Buttons
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Absenden")
        self.submit_button.clicked.connect(self.submit_feedback)
        button_layout.addWidget(self.submit_button)

        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def submit_feedback(self):
        rating = self.rating_combo.currentIndex() + 1
        comment = self.comment_edit.toPlainText().strip()

        # Save to file
        feedback_file = os.path.join(os.path.dirname(__file__), '..', 'feedback.txt')
        try:
            with open(feedback_file, 'a', encoding='utf-8') as f:
                timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
                f.write(f"{timestamp} - Rating: {rating} - Comment: {comment}\n")
            print(f"Feedback submitted: Rating {rating}, Comment: {comment}")
            QMessageBox.information(self, "Feedback", "Vielen Dank für Ihr Feedback!")
            self.accept()
        except Exception as e:
            print(f"Error saving feedback: {e}")
            QMessageBox.warning(self, "Fehler", "Feedback konnte nicht gespeichert werden.")
