from PySide6 import QtGui, QtCore, QtWidgets
import sys

class SleepTrackingWidget(QtWidgets.QFrame):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sleep Tracking")

        # Fonts
        quicksand_medium_title = QtGui.QFont("Quicksand Medium", 60)
        quicksand_medium_content = QtGui.QFont("Quicksand Medium", 32)
        quicksand_input = QtGui.QFont("Quicksand", 24)

        # Enable antialiasing for the fonts
        quicksand_medium_title.setStyleStrategy(QtGui.QFont.PreferAntialias)
        quicksand_medium_content.setStyleStrategy(QtGui.QFont.PreferAntialias)
        quicksand_input.setStyleStrategy(QtGui.QFont.PreferAntialias)

        # Title label
        self.title_label = QtWidgets.QLabel("Sleep Tracking")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setFont(quicksand_medium_title)

        # Main input field
        self.input = QtWidgets.QLineEdit()
        self.input.setFont(quicksand_input)
        self.input.setPlaceholderText("Input here")
        self.input.setMinimumHeight(50)
        self.input.setMaximumWidth(600)

        # Create the main layout
        layout = QtWidgets.QVBoxLayout()
        # Increase margins and spacing for better balance
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        # Add widgets to layout
        layout.addWidget(self.title_label)
        layout.addWidget(self.input, alignment=QtCore.Qt.AlignCenter)

        # Add the enter button
        self.enter_button = QtWidgets.QPushButton("Enter")
        self.enter_button.setFont(quicksand_input)
        self.enter_button.setMinimumHeight(50)
        self.enter_button.setMaximumWidth(200)
        layout.addWidget(self.enter_button, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(layout)

        # Improved stylesheet for a modern look with hover and focus effects
        self.setStyleSheet("""
            QFrame {
                background-color: #d493bd;
                color: #000000;
            }
            QLabel {
                color: #000000;
            }
            QLineEdit {
                background-color: #e59ecc;
                border: none;
                border-radius: 10px;
                color: #f3c0e1;
                padding: 10px;
            }
            QLineEdit:focus {
                border: 2px solid #f3c0e1;
            }
            QPushButton {
                background-color: #e59ecc;
                border: none;
                border-radius: 10px;
                color: #f3c0e1;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #f3c0e1;
                color: #e59ecc;
            }
        """)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SleepTrackingWidget()
    window.show()
    sys.exit(app.exec())