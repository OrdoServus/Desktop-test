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

3. **Wichtig:** Öffne `src/main.py` und passe die `TARGET_URL` an die tatsächliche URL deiner OrdoServus-Web-App an.

4. Anwendung starten:
   ```bash
   python -m src.main
   ```

## 📦 Ausführbare Datei erstellen

### Mit auto-py-to-exe (empfohlen, einfacher):

```bash
pip install auto-py-to-exe
auto-py-to-exe
```

**Dann im GUI:**
- Script Location: `src/main.py`
- One File: ✅
- Window Based: ✅
- Icon: `assets/icon.ico`
- Additional Files: `src`-Ordner hinzufügen → Destination: `src`
- Name: `OrdoServus Desktop`

Siehe **[BUILD_GUIDE.md](BUILD_GUIDE.md)** für detaillierte Schritt-für-Schritt-Anleitung mit Screenshots!

Alternativ lade die fertige Konfiguration `auto-py-to-exe-config.json` in auto-py-to-exe.

### Mit PyInstaller (Kommandozeile):

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=assets/icon.ico --name="OrdoServus Desktop" --add-data="src;src" src/main.py
```

Die .exe-Datei befindet sich dann im `dist/` bzw. `output/`-Ordner.

## 📁 Projektstruktur
```
Desktop-test/
├── src/                    # Quellcode
│   ├── __init__.py         # Paket-Initialisierung
│   ├── __version__.py      # Version
│   ├── main.py             # Einstiegspunkt
│   ├── ui.py               # GUI-Klasse
│   ├── settings.py         # Einstellungsverwaltung
│   └── updater.py          # Update-Modul
├── assets/                 # Ressourcen (Icons, etc.)
│   └── icon.ico            # Anwendungs-Icon (erstellen)
├── requirements.txt        # Python-Abhängigkeiten
├── README.md               # Diese Datei
├── CONTRIBUTING.md         # Beitragsrichtlinien
├── LICENSE                 # MIT-Lizenz
└── SECURITY.md             # Sicherheitsrichtlinien
```

## ⚙️ Konfiguration

### URL anpassen
Öffne `src/main.py` und ändere die `TARGET_URL`:
```python
TARGET_URL = "https://deine-ordoservus-url.de"
```

### Icon hinzufügen
Lege eine `icon.ico`-Datei im `assets/`-Verzeichnis ab. Du kannst Online-Konverter nutzen, um PNG zu ICO zu konvertieren.

## 🤝 Beitragen
Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Details zu Beiträgen.

## 🔒 Sicherheit
Siehe [SECURITY.md](SECURITY.md) für Sicherheitsrichtlinien.

## 📜 Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe [LICENSE](LICENSE) für Details.

## 📧 Kontakt
- E-Mail: ordo.servus@gmx.ch
- GitHub: [OrdoServus](https://github.com/OrdoServus)
