import sys
import os
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QLineEdit

class SignUpIntro(QtWidgets.QWidget):
    """A Sign up introduction page: Author James"""
    page_clicked = QtCore.Signal()

    def __init__(self):
        super().__init__()
        
        self.setMinimumSize(800, 600)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        font_path = os.path.join("resources", "fonts/quicksand", "Quicksand-Bold.ttf")
        QtGui.QFontDatabase.addApplicationFont(font_path)
        # Dynamic image paths
        base_dir = os.path.dirname(__file__)
        background_path = os.path.join("resources", "images", "Sign-up page (dark) (intro).png")

        # Load background
        self.background_pixmap = QtGui.QPixmap(background_path)
        if self.background_pixmap.isNull():
            print(f"Warning: Background image not found at {background_path}")

        # Labels
        self.main_label_hey = QtWidgets.QLabel("Now a bit about you!")
        self.main_label_hey.setAlignment(QtCore.Qt.AlignCenter)
        self.main_label_hey.setTextFormat(QtCore.Qt.RichText)

        self.main_label_glow = QtWidgets.QLabel("What would you like us to  call you", self)
        self.main_label_glow.setAlignment(QtCore.Qt.AlignCenter)
        self.main_label_glow.setTextFormat(QtCore.Qt.RichText)

        self.button = QtWidgets.QPushButton("enter", self)
        self.button.clicked.connect(self.on_button_click)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: rgba(246, 182, 118, 1);
                color: rgba(75, 74, 99, 1);
                border-radius: 20px;
                padding: 10px;
                font-size: 48px;
            }
        """)
        

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Input here")
        self.input_box.setAlignment(QtCore.Qt.AlignCenter)
        self.input_box.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 227, 155, 1);
                font-size: 40px;
                color: rgba(237, 216, 112, 1);
            }
        """)

        top_line_layout = QtWidgets.QVBoxLayout()
        top_line_layout.setAlignment(QtCore.Qt.AlignCenter)
        top_line_layout.addWidget(self.main_label_hey)
        top_line_layout.addSpacing(10)
        top_line_layout.addWidget(self.main_label_glow)
        top_line_layout.addSpacing(10)
        top_line_layout.addWidget(self.input_box)
        top_line_layout.addSpacing(10)
        top_line_layout.addWidget(self.button)
        

        # Main vertical layout
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        main_layout.addLayout(top_line_layout)
        self.setLayout(main_layout)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.page_clicked.emit()  # Emit signal with username

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

        self.main_label_hey.setFont(font1)
        self.main_label_glow.setFont(font2)

        button_font_size = max(20, min(int(self.width() * 0.05), 48))
        button_font = QtGui.QFont("Quicksand", button_font_size)
        button_font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.button.setFixedWidth(self.width() // 8)
        self.button.setFont(button_font)

        self.input_box.setFixedWidth(self.width() // 4)
        super().resizeEvent(event)

    
    def on_button_click(self):
        QtWidgets.QMessageBox.information(self, "Button Clicked", "You clicked the button!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    intro = SignUpIntro()
    intro.show()
    sys.exit(app.exec())

