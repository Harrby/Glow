from PySide6 import QtWidgets, QtGui, QtCore
import sys
import hashlib
import pymongo


def encrypt(password):
    return password
    # password_bytes = password.encode("utf-8")
    # hash_object = hashlib.sha256(password_bytes)
    # return hash_object.hexdigest()


class LoginScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LOGIN")
        self.setGeometry(100, 100, 900, 600)

        self.client = pymongo.MongoClient(
            "mongodb+srv://sam_user:9ireiEodVKBb3Owt@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster",
            tls=True,
            tlsAllowInvalidCertificates=True)
        self.db = self.client["mood_tracker"]
        self.collection = self.db["accounts"]

        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Title
        title = QtWidgets.QLabel("Login")
        title.setFont(QtGui.QFont("Quicksand", 32))
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # username Field
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Enter username:")
        self.username_input.setFont(QtGui.QFont("Quicksand", 14))
        self.username_input.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.username_input.setMinimumHeight(50)
        layout.addWidget(self.username_input)

        # Password Field
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Enter password:")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setFont(QtGui.QFont("Quicksand", 14))
        self.password_input.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.password_input.setMinimumHeight(50)
        layout.addWidget(self.password_input)

        # Login Button
        self.login_button = QtWidgets.QPushButton("Enter")
        self.login_button.setFont(QtGui.QFont("Quicksand", 14))
        self.login_button.clicked.connect(self.verify_login)
        layout.addWidget(self.login_button)

        # Error Messages
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
            self.error_label.setStyleSheet("color: green")
            # Proceed to the next screen (game_menu or new_password)
        else:
            self.error_label.setText("Username or password incorrect")
            self.error_label.setStyleSheet("color: red;")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginScreen()
    window.show()
    sys.exit(app.exec())
