import sys
import os
from PySide6 import QtGui, QtCore, QtWidgets


class SpeechWidget(QtWidgets.QWidget):
    """A page which introduces Glow.
    :author: James
    :created: 06-04-25
    :contributors:
        - Seb."""
    page_clicked = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.setMinimumSize(800, 600)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        # Load custom font
        font_path = os.path.join("resources", "fonts/quicksand", "Quicksand-Bold.ttf")
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
        self.font_family = families[0] if families else "Arial"

        # Background image
        base_dir = os.path.dirname(__file__)
        background_path = os.path.join(base_dir, "..", "resources", "images", "Sign-up page (dark) (intro).png")
        self.background_pixmap = QtGui.QPixmap(background_path)
        if self.background_pixmap.isNull():
            print(f"Warning: Background image not found at {background_path}")

        # Title label
        self.title = QtWidgets.QLabel("First, let me introduce Glow...", self)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setTextFormat(QtCore.Qt.RichText)

        # Speech text
        self.speech = QtWidgets.QLabel(
            "We are Glow!<br>"
            "Tiny fireflies, scattered throughout your journey, lighting the way to your goals. "
            "Glow is your personal companion — offering advice, motivation, and tailored suggestions "
            "to guide you forward. Wherever you are in your journey, we’ll be there, flickering with "
            "support and inspiration. You got this!",
            self
        )
        self.speech.setAlignment(QtCore.Qt.AlignCenter)
        self.speech.setWordWrap(True)
        self.speech.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        # Layout
        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        content_layout.addSpacing(90)
        content_layout.addWidget(self.title)
        content_layout.addSpacing(50)
        content_layout.addWidget(self.speech)
        content_layout.addSpacing(20)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

        # Force an initial resize so resizeEvent runs once
        QtCore.QTimer.singleShot(0, lambda: self.resize(self.size()))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = self.width()

        # Dynamic font sizes
        title_font = QtGui.QFont(self.font_family)
        title_font.setPointSize(max(20, int(w * 0.04)))
        self.title.setFont(title_font)

        speech_font = QtGui.QFont(self.font_family)
        speech_font.setPointSize(max(12, int(w * 0.02)))
        self.speech.setFont(speech_font)

    def mousePressEvent(self, event):
        # Emit immediately on any left-click
        if event.button() == QtCore.Qt.LeftButton:
            self.page_clicked.emit()

    def paintEvent(self, event):
        if not self.background_pixmap.isNull():
            painter = QtGui.QPainter(self)
            scaled = self.background_pixmap.scaled(
                self.size(),
                QtCore.Qt.KeepAspectRatioByExpanding,
                QtCore.Qt.SmoothTransformation
            )
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
            painter.end()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = SpeechWidget()
    widget.page_clicked.connect(lambda: print("Next page!"))
    widget.show()
    sys.exit(app.exec())
