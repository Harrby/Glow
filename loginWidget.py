from PySide6 import QtWidgets, QtGui, QtCore
import sys
import hashlib
import pymongo


def encrypt(password):
    # TODO: Replace with secure hashing (e.g., bcrypt) in production
    return password


class LoginWidget(QtWidgets.QWidget):
    """
        A QWidget-based login interface with MongoDB authentication and custom signal on success.
        Now styled with a calendar-themed background image and translucent, rounded form overlay.

        Author: Seb & Sam
        Updated: 2025-04-26
    """

    login_successful = QtCore.Signal(str)
    sign_up = QtCore.Signal()

    def __init__(self, context):
        super().__init__()
        self.context = context

        # Window setup
        self.setWindowTitle("LOGIN")
        self.setGeometry(100, 100, 900, 600)

        # Background label
        self.background_label = QtWidgets.QLabel(self)
        self.background_label.setPixmap(QtGui.QPixmap("resources/images/calenderBackground.png"))
        self.background_label.setScaledContents(True)
        self.background_label.lower()

        # Transparent overlay container for form
        self.container = QtWidgets.QWidget(self)

        # Apply styles to form elements
        self.setStyleSheet("""
            QLineEdit {
                background-color: #FFE39B;
                border: 1px solid #cccccc;
                border-radius: 8px;
                padding: 12px;
                font: 14pt Quicksand;
                font-color:black;
            }
            QPushButton {
                background-color: #F6B676;
                color: black;
                border-radius: 8px;
                padding: 12px;
                font: 14pt Quicksand;
            }
            QPushButton:hover {
                background-color: #FFE39B;
            }
            QLabel#error_label {
                font: 16pt Quicksand;
            }
            QLabel#title_label {
                font: bold 32pt Quicksand;
                color: white;
            }
        """)

        # Build UI inside container
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(150, 100, 150, 100)
        layout.setSpacing(20)

        # Title
        title = QtWidgets.QLabel("Login", objectName="title_label")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # Username Field
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Enter username...")
        self.username_input.setMinimumHeight(50)
        layout.addWidget(self.username_input)

        # Password Field
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Enter password...")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setMinimumHeight(50)
        layout.addWidget(self.password_input)

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.login_button = QtWidgets.QPushButton("Enter")
        self.login_button.clicked.connect(self.verify_login)
        button_layout.addWidget(self.login_button)

        self.sign_up_button = QtWidgets.QPushButton("Sign Up")
        self.sign_up_button.clicked.connect(self.sign_up.emit)
        button_layout.addWidget(self.sign_up_button)

        layout.addLayout(button_layout)

        # Error Message Label
        self.error_label = QtWidgets.QLabel(objectName="error_label")
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.error_label)

        layout.addStretch()
        self.container.setLayout(layout)

    def resizeEvent(self, event):
        # Ensure background and overlay fill the window
        size = self.size()
        self.background_label.setGeometry(0, 0, size.width(), size.height())
        self.container.setGeometry(0, 0, size.width(), size.height())
        return super().resizeEvent(event)

    def verify_login(self):
        username = self.username_input.text().strip()
        password = encrypt(self.password_input.text())

        user = self.collection.find_one({"username": username, "password": password})

        if user:
            self.error_label.setText("Login successful!")
            self.error_label.setStyleSheet("color: green;")
            self.context.username = username
            self.login_successful.emit(username)
        else:
            self.error_label.setText("Username or password incorrect")
            self.error_label.setStyleSheet("color: red; background-color: black;")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWidget(context=type('Ctx', (), {})())
    window.login_successful.connect(lambda u: print(f"Logged in as: {u}"))
    window.sign_up.connect(lambda: print("Signup invoked"))
    window.show()
    sys.exit(app.exec())
