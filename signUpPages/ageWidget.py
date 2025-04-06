import sys
import os
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QLineEdit

class AgeWidget(QtWidgets.QWidget):
    """A page asking for the user's age as part of the sign-up process.
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

        self.intro_message_label = QtWidgets.QLabel("Great! One last question...")
        self.intro_message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.intro_message_label.setTextFormat(QtCore.Qt.RichText)

        self.question_label = QtWidgets.QLabel("How old are you?", self)
        self.question_label.setAlignment(QtCore.Qt.AlignCenter)
        self.question_label.setTextFormat(QtCore.Qt.RichText)

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
                border-radius: 20px;
            }
        """)

        top_line_layout = QtWidgets.QVBoxLayout()
        top_line_layout.setAlignment(QtCore.Qt.AlignCenter)
        top_line_layout.addSpacing(40)
        top_line_layout.addWidget(self.intro_message_label)
        top_line_layout.addSpacing(50)
        top_line_layout.addWidget(self.question_label)
        top_line_layout.addSpacing(10)

        # Wrap input box in HBox to center it
        input_layout = QtWidgets.QHBoxLayout()
        input_layout.setAlignment(QtCore.Qt.AlignCenter)
        input_layout.addWidget(self.input_box)
        top_line_layout.addLayout(input_layout)
        top_line_layout.addSpacing(10)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignCenter)
        button_layout.addWidget(self.button)
        top_line_layout.addLayout(button_layout)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
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

        self.intro_message_label.setFont(font1)
        self.question_label.setFont(font2)

        button_font_size = max(20, min(int(self.width() * 0.05), 48))
        button_font = QtGui.QFont("Quicksand", button_font_size)
        button_font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.button.setFont(button_font)
        self.input_box.setFixedWidth(500)
        self.button.setFixedWidth(200)

        super().resizeEvent(event)

    def on_button_click(self):
        QtWidgets.QMessageBox.information(self, "Button Clicked", "You clicked the button!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    intro = AgeWidget()
    intro.show()
    sys.exit(app.exec())
