
from PySide6.QtGui import QShowEvent
from import_pyside6 import *
from gui.disigned_widget import OverlayWindow

class Clock(OverlayWindow):

    showed = Signal()
    def __init__(self):
        super().__init__()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("맑은 고딕", 20))
        self.w_label = QLabel()
        self.w_label.setAlignment(Qt.AlignCenter)
        self.w_label.setFont(QFont("맑은 고딕", 10))
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.w_label)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.title_bar.close_button.hide()
        self.title_bar.maximum_button.hide()

        self.setWindowTitle("보조 창")

    def showEvent(self, event: QShowEvent) -> None:
        self.showed.emit()
        return super().showEvent(event)
