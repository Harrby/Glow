import sys
import os
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QLineEdit

class EndWidget(QtWidgets.QWidget):
    """An introduction page that prompts the user to finalize their sign-up details and click a button to proceed.
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
        QtGui.QFontDatabase.addApplicationFont(font_path)
        
        base_dir = os.path.dirname(__file__)
        background_path = os.path.join("resources", "images", "Sign-up page (dark) (intro).png")

        self.background_pixmap = QtGui.QPixmap(background_path)
        if self.background_pixmap.isNull():
            print(f"Warning: Background image not found at {background_path}")

        self.intro_title_label = QtWidgets.QLabel("You're all set")
        self.intro_title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.intro_title_label.setTextFormat(QtCore.Qt.RichText)

        self.subtitle_label = QtWidgets.QLabel("We hope you love your experience with us", self)
        self.subtitle_label.setAlignment(QtCore.Qt.AlignCenter)
        self.subtitle_label.setTextFormat(QtCore.Qt.RichText)

        self.button = QtWidgets.QPushButton("Lets Glow", self)
        self.button.clicked.connect(self.on_button_click)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: rgba(252, 236, 174, 0.99);
                color: rgba(75, 74, 99, 1);
                border-radius: 20px;
                padding: 10px;
                font-size: 48px;
            }
        """)
        
        top_line_layout = QtWidgets.QVBoxLayout()
        top_line_layout.setAlignment(QtCore.Qt.AlignCenter)
        top_line_layout.addWidget(self.intro_title_label)
        top_line_layout.addSpacing(10)
        top_line_layout.addWidget(self.subtitle_label)
        top_line_layout.addSpacing(10)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignCenter)
        button_layout.addWidget(self.button)
        top_line_layout.addSpacing(100)
        top_line_layout.addLayout(button_layout)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignHCenter)
        main_layout.addLayout(top_line_layout)
        self.setLayout(main_layout)

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

    def resizeEvent(self, event):
        font_size_1 = max(20, int(self.width() * 0.04))
        font_size_2 = max(12, int(self.width() * 0.02))

        font1 = QtGui.QFont("Quicksand", font_size_1)
        font1.setStyleStrategy(QtGui.QFont.PreferAntialias)

        font2 = QtGui.QFont("Quicksand", font_size_2)
        font2.setStyleStrategy(QtGui.QFont.PreferAntialias)

        self.intro_title_label.setFont(font1)
        self.subtitle_label.setFont(font2)

        button_font_size = max(20, min(int(self.width() * 0.05), 48))
        button_font = QtGui.QFont("Quicksand", button_font_size)
        button_font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.button.setFont(button_font)
        self.button.setFixedWidth(300)

        super().resizeEvent(event)

    def on_button_click(self):
        QtWidgets.QMessageBox.information(self, "Button Clicked", "You clicked the button!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    intro = EndWidget()
    intro.show()
    sys.exit(app.exec())
