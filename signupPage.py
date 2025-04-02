from PySide6 import QtWidgets, QtGui, QtCore
from better_profanity import profanity
import re
import sys
import hashlib
import pymongo

def encrypt(password):
    return password  # Placeholder for actual encryption

class SignupScreen(QtWidgets.QWidget):  # Inherit from QWidget
    login_successful = QtCore.Signal(str)  # Define signal

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CREATE AN ACCOUNT")
        self.setGeometry(100, 100, 600, 600)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QtGui.QPalette.Window, QtGui.QColor("#4B4A63"))
        self.setPalette(p)

        self.client = pymongo.MongoClient(
            "mongodb+srv://sam_user:9ireiEodVKBb3Owt@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster",
            tls=True,
            tlsAllowInvalidCertificates=True
        )
        self.db = self.client["mood_tracker"]
        self.collection = self.db["accounts"]

        self.init_ui()

    def init_ui(self):
        central_widget = QtWidgets.QWidget(self)
        main_layout = QtWidgets.QVBoxLayout(central_widget)

        h_layout = QtWidgets.QHBoxLayout()
        layout = QtWidgets.QVBoxLayout()

        # Title
        title = QtWidgets.QLabel("Create an Account")
        title.setFont(QtGui.QFont("Quicksand", 32))
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # Firstname Field
        self.firstname_input = QtWidgets.QLineEdit()
        self.firstname_input.setPlaceholderText("Enter firstname:")
        self.firstname_input.setFont(QtGui.QFont("Quicksand", 14))
        self.firstname_input.setMinimumHeight(50)
        self.firstname_input.setMaximumWidth(245)
        self.firstname_input.setStyleSheet("background-color: #E4DCCF;")
        h_layout.addWidget(self.firstname_input)

        # Surname Field
        self.surname_input = QtWidgets.QLineEdit()
        self.surname_input.setPlaceholderText("Enter surname:")
        self.surname_input.setFont(QtGui.QFont("Quicksand", 14))
        self.surname_input.setMinimumHeight(50)
        self.surname_input.setMaximumWidth(245)
        self.surname_input.setStyleSheet("background-color: #E4DCCF;")
        h_layout.addWidget(self.surname_input)
        layout.addLayout(h_layout)

        # Username Field
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Enter username:")
        self.username_input.setFont(QtGui.QFont("Quicksand", 14))
        self.username_input.setMinimumHeight(50)
        self.username_input.setMaximumWidth(500)
        self.username_input.setStyleSheet("background-color: #E4DCCF;")
        layout.addWidget(self.username_input)

        # Password Field
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Enter password:")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setFont(QtGui.QFont("Quicksand", 14))
        self.password_input.setMinimumHeight(50)
        self.password_input.setMaximumWidth(500)
        self.password_input.setStyleSheet("background-color: #E4DCCF;")
        layout.addWidget(self.password_input)

        # Password Repeat Field
        self.password_repeat_input = QtWidgets.QLineEdit()
        self.password_repeat_input.setPlaceholderText("Re-enter password:")
        self.password_repeat_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_repeat_input.setFont(QtGui.QFont("Quicksand", 14))
        self.password_repeat_input.setMinimumHeight(50)
        self.password_repeat_input.setMaximumWidth(500)
        self.password_repeat_input.setStyleSheet("background-color: #E4DCCF;")
        layout.addWidget(self.password_repeat_input)

        # Signup Button
        self.signup_button = QtWidgets.QPushButton("Enter")
        self.signup_button.setFont(QtGui.QFont("Quicksand", 14))
        self.signup_button.clicked.connect(self.verify_signup)
        self.signup_button.setMinimumHeight(50)
        self.signup_button.setMaximumWidth(500)
        self.signup_button.setStyleSheet("background-color: #FFE39B;")
        layout.addWidget(self.signup_button)

        # Error Messages
        self.error_label = QtWidgets.QLabel()
        self.error_label.setFont(QtGui.QFont("Quicksand", 16))
        layout.addWidget(self.error_label)

        layout.addStretch()
        
        main_layout.addLayout(layout)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(main_layout)

    def contains_embedded_profanity(self, text):
        profanity.load_censor_words()
        words = re.findall(r'[a-zA-Z]+', text)  
        for word in words:
            ##FIX ME
            if profanity.contains_profanity(word):
                return True
        return False
    
    def verify_signup(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        password_repeat = self.password_repeat_input.text().strip()

        if password != password_repeat:
            self.error_label.setText("Passwords Do Not Match")
            self.error_label.setStyleSheet("color: red;")
            return
        
        if self.collection.find_one({"username": username}):  # Fixed checking existing user
            self.error_label.setText("Username Already Exists")
            self.error_label.setStyleSheet("color: red;") 
            return
        
        if self.contains_embedded_profanity(username):
            self.error_label.setText("Username Contains Prohibited Words")
            self.error_label.setStyleSheet("color: red;")
            return
        
        if username == "" or password == "":
            self.error_label.setText("Please Fill Out All Fields")
            self.error_label.setStyleSheet("color: red;")
            return
        # Save user to database
        self.collection.insert_one({
            "username": username,
            "password": encrypt(password),
            "firstname": self.firstname_input.text().strip(),
            "surname": self.surname_input.text().strip()
        })

        self.error_label.setText("Account Setup Successful")
        self.error_label.setStyleSheet("color: green")
        self.login_successful.emit(username)  # Emit signal with username

### **Main Function to Run Signup Page**
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = SignupScreen()
    window.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()