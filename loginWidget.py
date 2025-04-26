from PySide6 import QtWidgets, QtGui, QtCore
import sys
import os
import hashlib
import pymongo


def encrypt(password):
    # Example placeholder; replace with real hashing if needed
    return password


class LoginWidget(QtWidgets.QWidget):
    """
        A QWidget-based login interface with MongoDB authentication and custom signal on success.

        This widget presents a login form consisting of a username field, a password field (with obscured input),
        a login button, and dynamic error messaging. It authenticates users against a MongoDB Atlas database
        and emits a custom signal with the username upon successful login. The layout is styled for clarity and
        ease of use with large, accessible input fields and buttons.

        Attributes:
            username_input (QLineEdit): Input field for the user's username.
            password_input (QLineEdit): Input field for the user's password (masked).
            login_button (QPushButton): Button to submit the login form.
            error_label (QLabel): Displays success or failure messages.
            client (MongoClient): MongoDB client connection to the remote database.
            db (Database): MongoDB database instance for user accounts.
            collection (Collection): MongoDB collection containing user credentials.
            login_successful (Signal): Custom PySide signal emitted with the username on successful login.

        Methods:
            init_ui(): Initializes the layout and UI components.
            verify_login(): Verifies user credentials and emits a success signal if valid.

        Author: Seb & Sam
        Created: 2025-03-27
    """

    login_successful = QtCore.Signal(str)
    sign_up = QtCore.Signal()

    def __init__(self, context):
        super().__init__()

        self.client = pymongo.MongoClient(
            "mongodb+srv://sam_user:9ireiEodVKBb3Owt@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster",
            tls=True,
            tlsAllowInvalidCertificates=True
        )
        self.db = self.client["mood_tracker"]
        self.collection = self.db["accounts"]

        self.context = context
        self.setObjectName("LoginWidget")
        self.setWindowTitle("LOGIN")
        self.setGeometry(100, 100, 900, 600)

        # Load background pixmap
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_dir, 'resources', 'images', 'calenderBackground.png')
        if os.path.exists(img_path):
            self.background_pixmap = QtGui.QPixmap(img_path)
        else:
            print(f"[Warning] Background image not found at: {img_path}")
            self.background_pixmap = None

        self.init_ui()

    def paintEvent(self, event):
        if getattr(self, 'background_pixmap', None):
            painter = QtGui.QPainter(self)
            painter.drawPixmap(self.rect(), self.background_pixmap)
        super().paintEvent(event)

    def init_ui(self):
        # Global stylesheet for child widgets
        self.setStyleSheet("""
            QLineEdit {
                background: #FFE39B;
                border: 2px solid #ffffff;
                border-radius: 5px;
                padding: 10px;
                font-family: Quicksand;
                font-size: 14pt;
                color: black;
            }
            QPushButton {
                background-color: #F6B676;
                color: black;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-family: Quicksand;
                font-size: 14pt;
            }
            QPushButton:hover {
                background-color: #FFE39B;
            }
            QLabel {
                color: white;
                font-family: Quicksand;
            }""")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(250,250,250,250)

        # Title
        title = QtWidgets.QLabel("Login")
        title.setFont(QtGui.QFont("Quicksand", 32))
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # Username Field
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Enter username:")
        self.username_input.setMinimumHeight(50)
        layout.addWidget(self.username_input)

        # Password Field
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Enter password:")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setMinimumHeight(50)
        layout.addWidget(self.password_input)

        # Login Button
        self.login_button = QtWidgets.QPushButton("Enter")
        self.login_button.clicked.connect(self.verify_login)
        layout.addWidget(self.login_button)

        # Sign Up Button
        self.sign_up_button = QtWidgets.QPushButton("Sign Up")
        self.sign_up_button.clicked.connect(self.sign_up.emit)
        layout.addWidget(self.sign_up_button)

        # Error / Success Message
        self.error_label = QtWidgets.QLabel()
        self.error_label.setFont(QtGui.QFont("Quicksand", 16))
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.error_label)

        layout.addStretch()
        self.setLayout(layout)

    def verify_login(self):
        username = self.username_input.text()
        password = encrypt(self.password_input.text())

        user = self.collection.find_one({"username": username, "password": password})
        if user:
            self.error_label.setText("Login successful!")
            self.error_label.setStyleSheet("color: #00e676;")
            self.context.username = username
            self.login_successful.emit(username)
        else:
            self.error_label.setText("Username or password incorrect")
            self.error_label.setStyleSheet("color: #ff1744;")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWidget(context=None)
    window.login_successful.connect(lambda u: print(f"Logged in as: {u}"))
    window.sign_up.connect(lambda: print("Sign Up triggered"))
    window.show()
    sys.exit(app.exec())
