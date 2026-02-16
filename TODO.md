# TODO - Desktop-test Modifications

## Task: Simplify app, block external links, remove dark mode and downloads

### 1. Block external links (ui.py)
- [x] Modify CustomWebEnginePage.acceptNavigationRequest() to block external links instead of opening them

### 2. Remove Dark Mode
- [x] ui.py: Remove self.dark_mode variable and related code
- [x] ui.py: Remove toggle_dark_mode() method
- [x] ui.py: Remove apply_theme() method
- [x] ui.py: Remove dark mode menu item from create_menu()
- [x] ui.py: Remove dark mode from restore_settings() and save_settings()
- [x] settings.py: Remove get_dark_mode() and set_dark_mode() methods

### 3. Remove Download functionality
- [x] ui.py: Remove profile.downloadRequested.connect() in init_ui()
- [x] ui.py: Remove on_download_requested() method
- [x] ui.py: Remove download_finished() method
- [x] ui.py: Remove download_state_changed() method

### 4. Simplify
- [x] Clean up any unnecessary imports if any

## Status: ✅ ABGESCHLOSSEN

Alle Änderungen wurden erfolgreich vorgenommen:
- Externe Links werden jetzt blockiert (nicht im Browser geöffnet)
- Dark Mode wurde vollständig entfernt
- Download-Funktionalität wurde vollständig entfernt
- Die Anwendung wurde vereinfacht
