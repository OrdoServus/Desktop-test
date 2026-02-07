# Copyright (c) 2026 OrdoServus
# Licensed under the MIT License

from PyQt5.QtCore import QSettings

class AppSettings:
    def __init__(self, organization="OrdoServus", app_name="OrdoServus APP"):
        self.settings = QSettings(organization, app_name)

    def get_dark_mode(self):
        return self.settings.value("dark_mode", False, type=bool)

    def set_dark_mode(self, value):
        self.settings.setValue("dark_mode", value)

    def get_zoom_level(self):
        return self.settings.value("zoom_level", 1.0, type=float)

    def set_zoom_level(self, value):
        self.settings.setValue("zoom_level", value)

    def get_geometry(self):
        return self.settings.value("geometry")

    def set_geometry(self, value):
        self.settings.setValue("geometry", value)

    def save_geometry(self, widget):
        self.set_geometry(widget.saveGeometry())

    def restore_geometry(self, widget):
        geometry = self.get_geometry()
        if geometry:
            widget.restoreGeometry(geometry)
        else:
            widget.setGeometry(100, 100, 1200, 800)
