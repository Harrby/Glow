import sys
import os
from PySide6 import QtGui, QtCore, QtWidgets

class SpeechWidget(QtWidgets.QWidget):
    """A page which introduces glow.
    :author: James
    :created: 06-04-25
    :contributors:
        - Add your name here when you edit or maintain this class."""
    page_clicked = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.setMinimumSize(800, 600)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        font_path = os.path.join("resources", "fonts/quicksand", "Quicksand-Bold.ttf")
        font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
        families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
        self.font_family = families[0] if families else "Arial"
    

        base_dir = os.path.dirname(__file__)
        background_path = os.path.join("resources", "images", "Sign-up page (dark) (intro).png")

        self.background_pixmap = QtGui.QPixmap(background_path)
        if self.background_pixmap.isNull():
            print(f"Warning: Background image not found at {background_path}")

        # Title label
        self.title = QtWidgets.QLabel("First, let me introduce Glow...", self)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setTextFormat(QtCore.Qt.RichText)
        self.title.setFont(QtGui.QFont(self.font_family))
        
        # Speech label
        self.speech = QtWidgets.QLabel("""
        We are Glow!<br>
        Tiny fireflies, scattered throughout your journey, lighting the way to your goals. Glow is your personal companion — offering advice, motivation, and tailored suggestions to guide you forward. Wherever you are in your journey, we’ll be there, flickering with support and inspiration. You got this!
        """, self)
        self.speech.setAlignment(QtCore.Qt.AlignCenter)
        self.speech.setWordWrap(True)
        self.speech.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.speech.setFont(QtGui.QFont(self.font_family))

        # Content layout
        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        content_layout.addSpacing(90)
        content_layout.addWidget(self.title)
        content_layout.addSpacing(50)
        content_layout.addWidget(self.speech)
        content_layout.addSpacing(20)

        # Main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

        # Initial resize to set fonts and widths
        QtCore.QTimer.singleShot(0, self.update_fonts_and_widths)

    def update_fonts_and_widths(self):
        """Force initial update of fonts and widths"""
        self.resize(self.size())

    def resizeEvent(self, event):
        """Handle dynamic resizing of fonts and widths"""
        super().resizeEvent(event)
    
        # Calculate dynamic font sizes based on window height
        title_font_size = max(20, int(self.width() * 0.04))
        speech_font_size = max(12, int(self.width() * 0.02))

        # Update title font
        title_font = QtGui.QFont(self.font_family)
        title_font.setPointSize(title_font_size)
        self.title.setFont(title_font)

        # Update speech font
        speech_font = QtGui.QFont(self.font_family)
        speech_font.setPointSize(speech_font_size)
        self.speech.setFont(speech_font)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.page_clicked.emit()

    def paintEvent(self, event):
        if not self.background_pixmap.isNull():
            painter = QtGui.QPainter(self)
            scaled_pixmap = self.background_pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
            center_x = (self.width() - scaled_pixmap.width()) // 2
            center_y = (self.height() - scaled_pixmap.height()) // 2
            painter.drawPixmap(center_x, center_y, scaled_pixmap)
            painter.end()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    intro = SpeechWidget()
    intro.show()
    sys.exit(app.exec())