# ⛪ OrdoServus Desktop
**Der digitale Begleiter für Liturgie und Pastoral – als Desktop-Anwendung.**

OrdoServus Desktop ist eine native Desktop-Anwendung, die die OrdoServus-Web-App in einem eingebetteten Browser-Fenster läuft. Sie bietet eine nahtlose Erfahrung für liturgische Planung und Notizen, mit zusätzlichen Desktop-Features wie System-Tray, Dark Mode und Offline-Zugriff.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## ✨ Funktionen
- **Eingebettete Web-App:** Vollständiger Zugriff auf OrdoServus im Desktop-Fenster.
- **System-Tray-Integration:** Minimieren in die Taskleiste für Hintergrundbetrieb.
- **Dark Mode:** Umschaltbarer dunkler Modus für besseren Komfort.
- **Zoom-Steuerung:** Anpassbare Zoom-Stufen für die Web-Ansicht.
- **Automatische Updates:** Integrierte Update-Prüfung über GitHub Releases.
- **Datei-Downloads:** Direkter Download von Dateien aus der Web-App.
- **Lokale Einstellungen:** Persistente Speicherung von Präferenzen.

## 🚀 Technologie
- **Sprache:** Python 3.8+
- **GUI-Framework:** [PyQt5](https://pypi.org/project/PyQt5/) mit Qt WebEngine
- **Web-App:** Integriert [OrdoServus Web](https://github.com/flohulo/ordoservus)
- **Packaging:** PyInstaller für ausführbare Dateien
- **Lizenz:** MIT

## 🛠️ Installation & Nutzung

### Voraussetzungen
- Python 3.8 oder höher
- pip für Paketinstallation

### Installation
1. Repository klonen:
   ```bash
   git clone https://github.com/OrdoServus/Desktop-test.git
   cd Desktop-test
   ```

2. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

3. Anwendung starten:
   ```bash
   python src/main.py
   ```

## 📁 Projektstruktur
```
Desktop-test/
├── src/                    # Quellcode
│   ├── __version__.py      # Version
│   ├── main.py             # Einstiegspunkt
│   ├── ui.py               # GUI-Klasse
│   ├── settings.py         # Einstellungsverwaltung
│   └── updater.py          # Update-Modul
├── assets/                 # Ressourcen (Icons, etc.)
├── requirements.txt        # Python-Abhängigkeiten
├── README.md               # Diese Datei
├── CONTRIBUTING.md         # Beitragsrichtlinien
├── LICENSE                 # MIT-Lizenz
└── SECURITY.md             # Sicherheitsrichtlinien
```

## 🤝 Beitragen
Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Details zu Beiträgen.

## 📜 Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe [LICENSE](LICENSE) für Details.
