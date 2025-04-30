import sys
import os
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QLineEdit

class DetailsWidget(QtWidgets.QWidget):
    """A page asking for the user's username and password as part of the sign-up process.
    :author: James / Modified by [Your Name]
    :created: 06-04-25 (modified)
    :contributors:
        - Seb."""
    page_clicked = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.setMinimumSize(800, 600)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        # Add custom font
        font_path = os.path.join("resources", "fonts/quicksand", "Quicksand-Bold.ttf")
        QtGui.QFontDatabase.addApplicationFont(font_path)

        # Load background image
        base_dir = os.path.dirname(__file__)
        background_path = os.path.join("resources", "images", "Sign-up page (dark) (intro).png")
        self.background_pixmap = QtGui.QPixmap(background_path)
        if self.background_pixmap.isNull():
            print(f"Warning: Background image not found at {background_path}")

        # Intro and question labels
        self.intro_message_label = QtWidgets.QLabel("Let's define your account...")
        self.intro_message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.intro_message_label.setTextFormat(QtCore.Qt.RichText)

        self.question_label = QtWidgets.QLabel("What would you like your username and password to be?", self)
        self.question_label.setAlignment(QtCore.Qt.AlignCenter)
        self.question_label.setTextFormat(QtCore.Qt.RichText)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setAlignment(QtCore.Qt.AlignCenter)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 227, 155, 1);
                font-size: 40px;
                color: black;
                border-radius: 20px;
                padding: 10px;
            }
        """)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setAlignment(QtCore.Qt.AlignCenter)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 227, 155, 1);
                font-size: 40px;
                color: rgba(237, 216, 112, 1);
                border-radius: 20px;
                padding: 10px;
            }
        """)

        # Action button
        self.button = QtWidgets.QPushButton("Enter", self)
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

        # Main vertical layout to center content vertically and horizontally
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignCenter)
        
        # Add stretch before the content
        main_layout.addStretch()

        # Create a sub-layout for the labels and inputs
        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setAlignment(QtCore.Qt.AlignCenter)
        content_layout.addWidget(self.intro_message_label)
        content_layout.addSpacing(20)
        content_layout.addWidget(self.question_label)
        content_layout.addSpacing(30)

        # Input layout for username and password fields
        inputs_layout = QtWidgets.QVBoxLayout()
        inputs_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.username_input.setFixedWidth(500)
        self.password_input.setFixedWidth(500)
        inputs_layout.addWidget(self.username_input)
        inputs_layout.addSpacing(20)
        inputs_layout.addWidget(self.password_input)
        content_layout.addLayout(inputs_layout)
        content_layout.addSpacing(30)

        # Button layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.button.setFixedWidth(200)
        button_layout.addWidget(self.button)
        content_layout.addLayout(button_layout)

        # Add content to main layout
        main_layout.addLayout(content_layout)

        # Add stretch after the content to push it to the center vertically
        main_layout.addStretch()

        self.setLayout(main_layout)

    def paintEvent(self, event):
        if not self.background_pixmap.isNull():
            painter = QtGui.QPainter(self)
            scaled_pixmap = self.background_pixmap.scaled(
                self.size(), 
                QtCore.Qt.KeepAspectRatioByExpanding, 
                QtCore.Qt.SmoothTransformation
            )
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

        super().resizeEvent(event)

    def on_button_click(self):
        username = self.username_input.text()
        password = self.password_input.text()
        # Handle the username and password as needed.
        self.page_clicked.emit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DetailsWidget()
    window.page_clicked.connect(lambda: print("Next page!"))
    window.show()
    sys.exit(app.exec())
