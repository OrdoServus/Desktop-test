"""
Auto-Updater für die Web App
Überprüft GitHub Releases auf neue Versionen
"""

import requests
import json
import webbrowser
from packaging import version
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal

class UpdateChecker(QThread):
    """Background thread für Update-Check"""
    update_available = pyqtSignal(str, str, str)  # version, download_url, release_notes

    def __init__(self, current_version, github_repo):
        super().__init__()
        self.current_version = current_version
        self.github_repo = github_repo  # Format: "username/repo"
        self.update_found = False
    
    def run(self):
        """Prüft auf Updates"""
        try:
            # GitHub API: Latest Release abrufen
            api_url = f"https://api.github.com/repos/{self.github_repo}/releases/latest"
            response = requests.get(api_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                latest_version = data['tag_name'].lstrip('v')
                release_notes = data['body']
                
                # Download URL für .exe finden
                download_url = None
                for asset in data.get('assets', []):
                    if asset['name'].endswith('.exe'):
                        download_url = asset['browser_download_url']
                        break
                
                if not download_url:
                    download_url = data['html_url']  # Fallback: Release-Seite
                
                # Version vergleichen
                if version.parse(latest_version) > version.parse(self.current_version):
                    self.update_found = True
                    self.update_available.emit(latest_version, download_url, release_notes)
        except Exception as e:
            print(f"Update-Check fehlgeschlagen: {e}")

def show_update_dialog(parent, new_version, download_url, release_notes):
    """Zeigt Update-Dialog"""
    msg = QMessageBox(parent)
    msg.setWindowTitle("Update verfügbar")
    msg.setIcon(QMessageBox.Information)
    msg.setText(f"Eine neue Version ist verfügbar: v{new_version}")
    msg.setInformativeText("Möchtest du die neue Version herunterladen?")
    msg.setDetailedText(f"Was ist neu:\n\n{release_notes}")
    
    download_btn = msg.addButton("Herunterladen", QMessageBox.AcceptRole)
    msg.addButton("Später", QMessageBox.RejectRole)
    
    msg.exec_()
    
    if msg.clickedButton() == download_btn:
        webbrowser.open(download_url)

def check_for_updates(parent, current_version, github_repo, silent=False):
    """
    Startet Update-Check
    
    Args:
        parent: Parent Widget (für Dialog)
        current_version: Aktuelle Version (z.B. "1.0.0")
        github_repo: GitHub Repo (z.B. "username/web-app")
        silent: Wenn True, keine Meldung wenn kein Update verfügbar
    """
    checker = UpdateChecker(current_version, github_repo)
    
    def on_update_found(new_version, download_url, release_notes):
        show_update_dialog(parent, new_version, download_url, release_notes)
    
    def on_finished():
        if not silent and not checker.update_available:
            QMessageBox.information(
                parent,
                "Keine Updates",
                "Du verwendest bereits die neueste Version."
            )
    
    checker.update_available.connect(on_update_found)
    checker.finished.connect(on_finished)
    checker.start()
    
    return checker
