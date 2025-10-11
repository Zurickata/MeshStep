from PyQt5.QtWidgets import QDialog, QVBoxLayout
from PyQt5.QtCore import QUrl
try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView
except Exception:
    QWebEngineView = None
import os

class ManualDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manual de usuario")
        self.resize(800, 600)

        layout = QVBoxLayout(self)
        self.web_view = QWebEngineView(self)
        html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../manual.html"))
        self.web_view.load(QUrl.fromLocalFile(html_path))
        layout.addWidget(self.web_view)
        self.setLayout(layout)